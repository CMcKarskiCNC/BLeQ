# -*- coding: utf-8 -*-


from collections    import deque
from enum           import Enum
from .              import constants as const
from ..BLonitor     import BLonitor

LocalDEBUG = True

# types
class LogStatus(str, Enum):
    SUCCESS         = "success"
    WARNING         = "warning"
    ERROR           = "error"
    BLENDER_ERROR   = "Blender error"

class LogSender(str, Enum):
    BLEQ_APP        = "BleQ"
    BL_OPS          = "Blender"

class LogReciever(str, Enum):
    BLENDER_UI      = "Blender UI"
    BLonitor        = "BLonitor"
    BLEQ            = "BleQ"
    ALL             = "All"

# logger
class logger():
    LogQ = deque()
 
    @staticmethod
    def clear():
        logger.LogQ.clear()
    
    @staticmethod
    def add(status: LogStatus, message: str, sender: LogSender = None, reciever: LogReciever = None):
        # set optionals
        if not sender:
            sender = "Unknown"
        if not reciever:
            reciever = LogReciever.ALL
        # blender UI
        if reciever == LogReciever.BLENDER_UI or reciever == LogReciever.ALL:
            logger.LogQ.append((status, message))
        # BLonitor
        if reciever == LogReciever.BLonitor or reciever == LogReciever.ALL:
            BLonitor.add_blonitor_message(sender, status, message)

    @staticmethod
    def print_log(operator=None):      
        # Get all messages from the queue
        messages = []
        while logger.LogQ:
            try:
                messages.append(logger.LogQ.popleft())
            except:
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
