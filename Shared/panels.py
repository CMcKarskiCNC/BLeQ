# -*- coding: utf-8 -*-

import bpy # type: ignore

from .              import constants    as const
from ..BLeQSender   import BLeQSender   as BSender

class EXTERNAL_PT_SETUP(bpy.types.Panel):
    bl_label        = "Setup / Support"
    bl_order        = 0
    bl_idname       = "EXTERNAL_PT_00_setup"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"

    def draw(self, context):
        layout = self.layout

        layout.label(text="BLeQ App:")
        layout.operator("external.open_bleq_website",    icon='URL')
        layout.operator("external.open_bleq_dllink",     icon='URL')
        layout.label(text="Git / Support:")
        layout.operator("external.open_git_website",     icon='URL')
        layout.operator("external.open_support_email",   icon='QUESTION')

class EXTERNAL_PT_bleq_sender(bpy.types.Panel):
    bl_label        = "BLeQSender"
    bl_order        = 1
    bl_idname       = "EXTERNAL_PT_01_bsender"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout  = self.layout
        wm      = context.window_manager

        rowenabler      = not BSender._queue_state["is_rendering"]

        row             = layout.row()
        row.enabled     = rowenabler
        row.template_list(
            "BLEQ_UL_string_list",      # 1. UIList-Type
            "",                         # 2. List-ID
            wm,                         # 3. Dataobject list
            "bleq_string_list",         # 4. Property-Name list
            wm,                         # 5. Dataobject index
            "bleq_string_list_index"    # 6. Property-Name index
        )

        layout.separator()
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("render.bleq_add"              , icon='ADD')
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("render.bleq_add_last"         , icon='ADD')
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("render.bleq_add_all_scenes"   , icon='ADD')

        layout.separator()
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("render.bleq_remove_sel"       , icon='REMOVE')
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("render.bleq_remove_files"     , icon='REMOVE')

        layout.separator()
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("render.bleq_start"            , icon='PLAY')
        row             = layout.row()        
        row.enabled     = False
        row.alert       = not rowenabler
        row.operator("render.bleq_stop"             , icon='QUIT')

class EXTERNAL_PT_blini_tools(bpy.types.Panel):
    bl_label        = "BLiniTools"
    bl_order        = 2
    bl_idname       = "EXTERNAL_PT_02_blinitools"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Coming soon:")
        self.layout.label(text="Small useful tools for blender")

class EXTERNAL_PT_bleq_page(bpy.types.Panel):
    bl_label        = "BLeQPage"
    bl_order        = 3
    bl_idname       = "EXTERNAL_PT_03_bpage"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Coming soon:")
        self.layout.label(text="3D webpages made in blender")
        self.layout.label(text="No coding, just creating")

class EXTERNAL_PT_hardware_monitor(bpy.types.Panel):
    bl_label        = "BLonitor"
    bl_order        = 4
    bl_idname       = "EXTERNAL_PT_04_blonitor"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Coming soon:")
        self.layout.label(text="Hardware monitoring in Blender")

# register grouping
_UTIL_CLASSES = (
    EXTERNAL_PT_SETUP,
    EXTERNAL_PT_bleq_sender,
    EXTERNAL_PT_blini_tools,
    EXTERNAL_PT_bleq_page,
    EXTERNAL_PT_hardware_monitor,
)

def register():
    # classes
    for cls in _UTIL_CLASSES:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_UTIL_CLASSES):
        bpy.utils.unregister_class(cls)