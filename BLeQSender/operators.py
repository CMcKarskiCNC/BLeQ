# -*- coding: utf-8 -*-

import bpy # type: ignore

from ..Shared   import logger       as log
from ..Shared   import constants    as const
from .          import BLeQSender   as BSender

# string item for the render queue list
class BLEQ_StringItem(bpy.types.PropertyGroup):
    filepath:       bpy.props.StringProperty(name="Filepath",   default="") # type: ignore
    scene_name:     bpy.props.StringProperty(name="Scene",      default="") # type: ignore
    camera_name:    bpy.props.StringProperty(name="Camera",     default="") # type: ignore
    name:           bpy.props.StringProperty(name="Name",       default="") # type: ignore

# string list UI
class BLEQ_UL_string_list(bpy.types.UIList):
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

class BUT_Add_Scenes(bpy.types.Operator):
    bl_idname       = "render.bleq_add_all_scenes"
    bl_label        = "Add All"
    bl_description  = "Add all scenes (with selected cam)"

    def execute(self, context):
        if not bpy.data.filepath:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot add to queue.")
            log.logger.print_log(self)
            return {'CANCELLED'}

        BSender.add_queue_all_scenes()
        
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
        if not bpy.data.filepath or bpy.data.is_dirty:
            log.logger.add(log.LogStatus.WARNING, "File not saved - cannot start queue.")
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


# register grouping
_UTIL_CLASSES =(
    BLEQ_StringItem,
    BLEQ_UL_string_list,
    BUT_Stop,
    BUT_Start,
    BUT_Add_Scenes,
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
        bpy.utils.register_class(cls)
    
    # properties
    for prop in _WM_PROPERTIES:
        prop_name = prop["name"]
        if not hasattr(bpy.types.WindowManager, prop_name):
            print(f"register Property / BLeQSender / operator: {prop_name} is already registered. Will be overwritten")
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


def unregister():
    # Remove properties
    for prop in reversed(_WM_PROPERTIES):
        prop_name = prop["name"]
        delattr(bpy.types.WindowManager, prop_name)
    
    # Unregister classes
    for cls in reversed(_UTIL_CLASSES):
        bpy.utils.unregister_class(cls)