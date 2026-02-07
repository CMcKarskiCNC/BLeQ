# -*- coding: utf-8 -*-

import bpy # type: ignore

from .              import constants    as const
from ..BLeQSender   import BLeQSender   as BSender
from ..BLonitor     import BLonitor

class BLEQ_PT_setup_panel(bpy.types.Panel):
    bl_idname       = "BLEQ_PT_00_setup_panel"
    bl_label        = "Setup / Support"
    bl_order        = 0
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"

    def draw(self, context):
        layout = self.layout

        layout.label(text="BLeQ Tutorial:")
        row         = layout.row()
        row.enabled = False
        row.operator("bleq.open_bleq_tutorial",         icon='URL')
        layout.label(text="Git / Support:")
        layout.operator("bleq.open_git_website",        icon='URL')
        layout.operator("bleq.open_support_email",      icon='QUESTION')

class BLEQ_PT_bleqsender_panel(bpy.types.Panel):
    bl_idname       = "BLEQ_PT_01_bleqsender_panel"
    bl_label        = "BLeQSender"
    bl_order        = 1
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout      = self.layout
        wm          = context.window_manager
        rowenabler  = not BSender._queue_state["is_rendering"]

        # list
        row             = layout.row()
        row.enabled     = rowenabler
        row.template_list(
            "BLEQ_UL_bleqsenderlist",   # 1. UIList-Type
            "",                         # 2. List-ID
            wm,                         # 3. Dataobject list
            "bleq_string_list",         # 4. Property-Name list
            wm,                         # 5. Dataobject index
            "bleq_string_list_index"    # 6. Property-Name index
        )

        # add
        layout.separator()
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("bleq.bsender_add"             , icon='ADD')
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("bleq.bsender_add_last"        , icon='ADD')
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("bleq.bsender_add_scenes"      , icon='ADD')

        # remove
        layout.separator()
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("bleq.bsender_remove_selected" , icon='REMOVE')
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("bleq.bsender_remove_files"    , icon='REMOVE')

        # start / stop
        layout.separator()
        row             = layout.row()
        row.enabled     = rowenabler
        row.operator("bleq.bsender_start"           , icon='PLAY')
        row             = layout.row()        
        row.enabled     = False
        row.alert       = not rowenabler
        row.operator("bleq.bsender_stop"             , icon='QUIT')

class BLEQ_PT_blinitools_panel(bpy.types.Panel):
    bl_idname       = "BLEQ_PT_02_blinitools_panel"
    bl_label        = "BLiniTools"
    bl_order        = 2
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Coming soon:")
        self.layout.label(text="Small useful tools for blender")

class BLEQ_PT_bleqpage_panel(bpy.types.Panel):
    bl_idname       = "BLEQ_PT_03_bleqpage_panel"
    bl_label        = "BLeQPage"
    bl_order        = 3
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"
    bl_options      = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Coming soon:")
        self.layout.label(text="3D webpages made in blender")
        self.layout.label(text="No coding, just creating")

class BLEQ_PT_blonitor_panel(bpy.types.Panel):
    bl_idname       = "BLEQ_PT_04_blonitor_panel"
    bl_label        = "BLonitor"
    bl_order        = 4
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "BLeQ"

    def draw(self, context):
        wm          = context.window_manager
        layout      = self.layout
        box         = layout.box()
        box.scale_y = 0.6
        box.template_list(
            "BLEQ_UL_blonitorlist",     # 1. UIList-Type
            "",                         # 2. List-ID
            wm,                         # 3. Dataobject list
            "bleq_blonitor_list",       # 4. Property-Name list
            wm,                         # 5. Dataobject index
            "bleq_blonitor_index",      # 6. Property-Name index
            rows    = BLonitor.MAXBLONITOR_ITEMS,
            maxrows = BLonitor.MAXBLONITOR_ITEMS,
            #type    = 'COMPACT'
        )

# register grouping
_UTIL_CLASSES = (
    BLEQ_PT_setup_panel,
    BLEQ_PT_bleqsender_panel,
    BLEQ_PT_blinitools_panel,
    BLEQ_PT_bleqpage_panel,
    BLEQ_PT_blonitor_panel,
)

# registration
def register():
    const.regfunction(_UTIL_CLASSES)

def unregister():
    const.unregfunction(_UTIL_CLASSES)