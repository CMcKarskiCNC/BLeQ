# -*- coding: utf-8 -*-

import bpy # type: ignore

from ..Shared   import logger       as log
from ..Shared   import constants    as const
from .          import BLeQSender   as BSender

# string item for the render queue list
class BLEQ_StringItem(bpy.types.PropertyGroup):
    filepath:    bpy.props.StringProperty(name="Filepath",    default="") # type: ignore
    scene_name:  bpy.props.StringProperty(name="Scene",       default="") # type: ignore
    camera_name: bpy.props.StringProperty(name="Camera",      default="") # type: ignore

# string list UI
class BLEQ_UL_string_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, "filepath",    text="", emboss=False)
        row.prop(item, "scene_name",  text="", emboss=False)
        row.prop(item, "camera_name", text="", emboss=False)

    def draw_filter(self, context, layout):
        # no Filter-UI
        pass

    def filter_items(self, context, data, propname):
        # no Filter-UI no sorting
        items = getattr(data, propname)
        return [], []

class BUT_Add(bpy.types.Operator):
    bl_idname       = "render.bleq_add"
    bl_label        = "Add Behind"
    bl_description  = "Add blend file to BLeQ behind current rendered file"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.")
            log.logger.print_log(self)
            return {'CANCELLED'}
        
        BSender.add_queue_file()

        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Add button pressed.")
        log.logger.print_log(self)

        return {'FINISHED'}

class BUT_Add_Last(bpy.types.Operator):
    bl_idname       = "render.bleq_add_last"
    bl_label        = "Add Last"
    bl_description  = "Add current blend file to the end of BLeQ render queue"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.")
            log.logger.print_log(self)
            return {'CANCELLED'}

        BSender.add_queue_file_last()
        
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Add Last button pressed.")
        log.logger.print_log(self)
        return {'FINISHED'}

class BUT_Remove_Selected(bpy.types.Operator):
    bl_idname       = "render.bleq_remove_sel"
    bl_label        = "Remove selected"
    bl_description  = "Remove selected file from queue"

    def execute(self, context):
        BSender.remove_selected_queue_file()

        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Remove Setting button pressed.")
        log.logger.print_log(self)
        return {'FINISHED'}

class BUT_Remove_Files(bpy.types.Operator):
    bl_idname       = "render.bleq_remove_files"
    bl_label        = "Remove All"
    bl_description  = "Remove (all) current blend files from BLeQ render queue"

    def execute(self, context):

        BSender.remove_queue_files()
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Remove Files button pressed.")
        log.logger.print_log(self)
        return {'FINISHED'}

class BUT_Start(bpy.types.Operator):
    bl_idname       = "render.bleq_start"
    bl_label        = "Start Queue"
    bl_description  = "Start BLeQ render queue processing"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.")
            log.logger.print_log(self)
            return {'CANCELLED'}

        BSender.start_queue_render()
       
        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Start button pressed.")
        log.logger.print_log(self)
        return {'FINISHED'}

class BUT_Stop(bpy.types.Operator):
    bl_idname       = "render.bleq_stop"
    bl_label        = "Stop Queue (ESC)"
    bl_description  = "Stop BLeQ render queue processing (only with BLeQApp)"

    def execute(self, context):
        BSender.stop_queue_render()

        log.logger.add(log.LogStatus.SUCCESS, "BLeQ Stop button pressed.")
        log.logger.print_log(self)
        return {'FINISHED'}

_UTIL_CLASSES =(
    BLEQ_StringItem,
    BLEQ_UL_string_list,
    BUT_Stop,
    BUT_Start,
    BUT_Remove_Files,
    BUT_Remove_Selected,
    BUT_Add_Last,
    BUT_Add,
)

_WM_PROPERTIES = (
    {
        "name":         "bleq_string_list",
        "type":         "collection",
        "prop_type":    BLEQ_StringItem,
    },
    {
        "name":         "bleq_string_list_index",
        "type":         "int",
        "default":      0,
        "description":  "Index"
    },
    {
        "name":         "bleq_use_app",
        "type":         "bool",
        "default":      False,
        "description":  "use BLeQ App"
    },
)

def register():
    # classes
    for cls in _UTIL_CLASSES:
        try:
            bpy.utils.register_class(cls)
        except RuntimeError as e:
            print(f"Re-registering {cls.__name__}: {e}")
            try:
                bpy.utils.unregister_class(cls)
                bpy.utils.register_class(cls)
            except Exception as ex:
                print(f"Failed to re-register {cls.__name__}: {ex}")
    
    # properties
    for prop in _WM_PROPERTIES:
        prop_name = prop["name"]
        if not hasattr(bpy.types.WindowManager, prop_name):
            if prop["type"] == "collection":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.CollectionProperty(type=prop["prop_type"]))
            elif prop["type"] == "int":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.IntProperty(
                    name    =prop.get("description", ""),
                    default =prop.get("default", 0)))
            elif prop["type"] == "bool":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.BoolProperty(
                    name        =prop.get("description", ""),
                    default     =prop.get("default", False),
                    description =prop.get("description", "")))
        else:
            print(f"register Property / BLeQSender / operator: {prop_name} is already registered.")

def unregister():
    # Remove properties
    for prop in reversed(_WM_PROPERTIES):
        if hasattr(bpy.types.WindowManager, prop["name"]):
            delattr(bpy.types.WindowManager, prop["name"])
    
    # Unregister classes
    for cls in reversed(_UTIL_CLASSES):
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)