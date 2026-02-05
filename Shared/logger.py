# -*- coding: utf-8 -*-

from pyexpat.errors import messages
import queue
import bpy      # type: ignore

from enum   import Enum
from re     import DEBUG
from .      import constants as const

LocalDEBUG = True

class LogStatus(str, Enum):
    SUCCESS         = "success"
    WARNING         = "warning"
    ERROR           = "error"
    BLENDER_ERROR   = "Blender error"

class logger():
    LogQ = queue.Queue()
 
    @staticmethod
    def clear():
        while not logger.LogQ.empty():
            try:
                logger.LogQ.get_nowait()
            except queue.Empty:
                break
    
    @staticmethod
    def add(status: LogStatus, message: str):
        logger.LogQ.put((status, message))

    @staticmethod
    def print_log(operator=None):      
        # Get all messages from the queue
        messages = []
        while not logger.LogQ.empty():
            try:
                messages.append(logger.LogQ.get_nowait())
            except queue.Empty:
                break
        if not messages:
            if const.DEBUG_MODE or LocalDEBUG:
                logger.dbprint("print_log", "empty list")
            return True
        
        # get all statuses
        statuses = [msg[0] if len(msg) > 1 else "unknown" for msg in messages]
        
        # set overall status
        if all(status == LogStatus.SUCCESS for status in statuses):
            overall_status  = LogStatus.SUCCESS
            report_type     = 'INFO'
        elif all(status == LogStatus.WARNING for status in statuses):
            overall_status  = LogStatus.WARNING
            report_type     = 'WARNING'
        elif any(status == LogStatus.ERROR for status in statuses) or any(status == LogStatus.BLENDER_ERROR for status in statuses):
                overall_status  = LogStatus.ERROR
                report_type     = 'ERROR'
        else:
            overall_status  = "mixed"
            report_type     = 'INFO'
        
        multiline_message = " |\n".join([msg[1] if len(msg) > 1 else "unknown" for msg in messages])
        multiline_message = f"\n{multiline_message}\n"
                
        if operator:
            if overall_status == LogStatus.ERROR:
                operator.report({report_type}, f"BleQ: {multiline_message}")
            elif overall_status == LogStatus.BLENDER_ERROR:
                operator.report({report_type}, f"Blender: {multiline_message}")
            else:
                operator.report({report_type}, multiline_message)

    @staticmethod
    def dbprint(Sender, message):
        global LocalDEBUG
        if const.DEBUG_MODE or LocalDEBUG:
            print(f"DEBUG  | {Sender}:\n         {message}")
