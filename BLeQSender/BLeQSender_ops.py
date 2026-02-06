# -*- coding: utf-8 -*-

import bpy # type: ignore

from ..Shared   import logger       as log
from ..Shared   import constants    as const
from .          import BLeQSender   as BSender

# string item for the render queue list
class BLEQ_bleqsenderitem(bpy.types.PropertyGroup):
    filepath:       bpy.props.StringProperty(name="Filepath",   default="") # type: ignore
    scene_name:     bpy.props.StringProperty(name="Scene",      default="") # type: ignore
    camera_name:    bpy.props.StringProperty(name="Camera",     default="") # type: ignore
    name:           bpy.props.StringProperty(name="Name",       default="") # type: ignore

# string list UI
class BLEQ_UL_bleqsenderlist(bpy.types.UIList):
    show_path:  bpy.props.BoolProperty( name="Show Path",   default=False,  description="Show filepath column")     # type: ignore
    show_name:  bpy.props.BoolProperty( name="Show Name",   default=False,  description="Show Name column")         # type: ignore
    show_cam:   bpy.props.BoolProperty( name="Show Cam",    default=True,   description="Show Camera column")       # type: ignore
    show_scene: bpy.props.BoolProperty( name="Show Scene",  default=True,   description="Show Scene column")        # type: ignore

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        if self.show_path:
            row.prop(item, "filepath",      text="", emboss=False)
        if self.show_scene:
            row.prop(item, "scene_name",    text="", emboss=False)
        if self.show_cam:
            row.prop(item, "camera_name",   text="", emboss=False)
        if self.show_name:
            row.prop(item, "name",          text="", emboss=False)

    def draw_filter(self, context, layout):
        row = layout.row(align=True)
        row.prop(self, "show_path",     text="Path",    toggle=True, icon='FILE_FOLDER')
        row.prop(self, "show_scene",    text="Scene",   toggle=True, icon='SCENE_DATA')
        row.prop(self, "show_cam",      text="Cam",     toggle=True, icon='CAMERA_DATA')
        row.prop(self, "show_name",     text="Name",    toggle=True, icon='SORTALPHA')

    def filter_items(self, context, data, propname):
        items = getattr(data, propname)
        return [], []

# buttons
class BLEQ_OT_bsender_add(bpy.types.Operator):
    bl_idname       = "bleq.bsender_add"
    bl_label        = "Add Behind"
    bl_description  = "Add blend file to BLeQ behind current rendered file"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
            log.logger.print_log(self)
            return {'CANCELLED'}
        
        BSender.add_queue_file()

        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Add button pressed.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
        log.logger.print_log(self)

        return {'FINISHED'}

class BLEQ_OT_bsender_add_last(bpy.types.Operator):
    bl_idname       = "bleq.bsender_add_last"
    bl_label        = "Add Last"
    bl_description  = "Add current blend file to the end of BLeQ render queue"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
            log.logger.print_log(self)
            return {'CANCELLED'}

        BSender.add_queue_file_last()
        
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Add Last button pressed.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
        log.logger.print_log(self)
        return {'FINISHED'}

class BLEQ_OT_bsender_add_scenes(bpy.types.Operator):
    bl_idname       = "bleq.bsender_add_scenes"
    bl_label        = "Add All"
    bl_description  = "Add all scenes (with selected cam)"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
            log.logger.print_log(self)
            return {'CANCELLED'}

        BSender.add_queue_all_scenes()
        
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Add Last button pressed.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
        log.logger.print_log(self)
        return {'FINISHED'}

class BLEQ_OT_bsender_remove_selected(bpy.types.Operator):
    bl_idname       = "bleq.bsender_remove_selected"
    bl_label        = "Remove selected"
    bl_description  = "Remove selected file from queue"

    def execute(self, context):
        BSender.remove_selected_queue_file()

        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Remove Setting button pressed.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
        log.logger.print_log(self)
        return {'FINISHED'}

class BLEQ_OT_bsender_remove_files(bpy.types.Operator):
    bl_idname       = "bleq.bsender_remove_files"
    bl_label        = "Remove All"
    bl_description  = "Remove (all) current blend files from BLeQ render queue"

    def execute(self, context):

        BSender.remove_queue_files()
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Remove Files button pressed.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
        log.logger.print_log(self)
        return {'FINISHED'}

class BLEQ_OT_bsender_start(bpy.types.Operator):
    bl_idname       = "bleq.bsender_start"
    bl_label        = "Start Queue"
    bl_description  = "Start BLeQ render queue processing"

    def execute(self, context):
        if not bpy.data.filepath or bpy.data.is_dirty:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot start queue.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
            log.logger.print_log(self)
            return {'CANCELLED'}

        BSender.start_queue_render()
       
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Start button pressed.","Start Queue")
        log.logger.print_log(self)
        return {'FINISHED'}

class BLEQ_OT_bsender_stop(bpy.types.Operator):
    bl_idname       = "bleq.bsender_stop"
    bl_label        = "Stop Queue (ESC)"
    bl_description  = "Stop BLeQ render queue processing (only with BLeQApp)"

    def execute(self, context):
        BSender.stop_queue_render()

        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Stop button pressed.", log.LogSender.BL_OPS, log.LogReciever.BLENDER_UI)
        log.logger.print_log(self)
        return {'FINISHED'}


# register grouping
_UTIL_CLASSES =(
    BLEQ_bleqsenderitem,
    BLEQ_UL_bleqsenderlist,
    BLEQ_OT_bsender_add,
    BLEQ_OT_bsender_add_last,
    BLEQ_OT_bsender_add_scenes,
    BLEQ_OT_bsender_remove_selected,
    BLEQ_OT_bsender_remove_files,
    BLEQ_OT_bsender_start,
    BLEQ_OT_bsender_stop,
)

_WM_PROPERTIES = (
    {
        "name":         "bleq_string_list",
        "UI_Name":      "Render Queue",
        "type":         "collection",
        "prop_type":    BLEQ_bleqsenderitem,
    },
    {
        "name":         "bleq_string_list_index",
        "UI_Name":      "Index Render Queue",
        "type":         "int",
        "default":      0,
        "description":  "Index"
    },
    {
        "name":         "bleq_progress_render",
        "UI_Name":      "Progress Render",
        "type":         "float",
        "subtype":      "PERCENTAGE",
        "min":          0,
        "max":          100,
        "description":  "shows progress of current render"
    },
    {
        "name":         "bleq_progress_all",
        "UI_Name":      "Progress Queue",
        "type":         "float",
        "subtype":      "PERCENTAGE",
        "min":          0,
        "max":          100,
        "description":  "shows progress of queue"
    },
)

# registration
def register():
    const.regfunction(_UTIL_CLASSES, _WM_PROPERTIES)

def unregister():
    const.unregfunction(_UTIL_CLASSES, _WM_PROPERTIES)