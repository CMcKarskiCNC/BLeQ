# -*- coding: utf-8 -*-

import bpy  # type: ignore

from ..Shared   import constants    as const

# message list UI
MAXBLONITOR_ITEMS = 5


def add_blonitor_message(sender: str, status: str, message: str):
    wm = bpy.context.window_manager
    # new item
    item            = wm.bleq_blonitor_list.add()
    item.sender     = sender
    item.status     = status
    item.message    = message
    wm.bleq_blonitor_list.move(len(wm.bleq_blonitor_list) - 1, 0)
    # remove old messages
    while len(wm.bleq_blonitor_list) > MAXBLONITOR_ITEMS:
        wm.bleq_blonitor_list.remove(len(wm.bleq_blonitor_list) - 1)

class BLEQ_blonitoritem(bpy.types.PropertyGroup):
    sender:     bpy.props.StringProperty(name="sender",     default="") # type: ignore
    status:     bpy.props.StringProperty(name="status",     default="") # type: ignore
    message:    bpy.props.StringProperty(name="message",    default="") # type: ignore

class BLEQ_UL_blonitorlist(bpy.types.UIList):
    show_sender:    bpy.props.BoolProperty( name="Show Sender",     default=False,  description="Show Sender column")       # type: ignore
    show_status:    bpy.props.BoolProperty( name="Show Status",     default=False,  description="Show Status column")       # type: ignore
    show_message:   bpy.props.BoolProperty( name="Show Message",    default=True,   description="Show Message column")      # type: ignore

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.scale_y = 1 
        row = layout.row(align=True)
        row.alignment = 'LEFT'  # oder 'CENTER' / 'RIGHT' 
        row = layout.row()
        if self.show_sender:
            row.prop(item, "sender",    text="", emboss=False)
        if self.show_status:
            row.prop(item, "status",    text="", emboss=False)
        if self.show_message:
            row.prop(item, "message",   text="", emboss=False)

    def draw_filter(self, context, layout):
        row = layout.row(align=True)
        row.prop(self, "show_sender",   text="Sender",  toggle=True, icon='USER')
        row.prop(self, "show_status",   text="Status",  toggle=True, icon='INFO')
        row.prop(self, "show_message",  text="Message", toggle=True, icon='TEXT')

    def filter_items(self, context, data, propname):
        items = getattr(data, propname)
        return [], []


# register grouping
_UTIL_CLASSES =(
    BLEQ_blonitoritem,
    BLEQ_UL_blonitorlist,
)

_WM_PROPERTIES =(
    {
        "name":         "bleq_blonitor_list",
        "UI_Name":      "BLonitor Messages",
        "type":         "collection",
        "prop_type":    BLEQ_blonitoritem,
    },
    {
        "name":         "bleq_blonitor_index",
        "UI_Name":      "Index Messages",
        "type":         "int",
        "default":      0,
        "description":  "Index"
    },
)

# registration
def register():
    const.regfunction(_UTIL_CLASSES, _WM_PROPERTIES)

def unregister():
    const.unregfunction(_UTIL_CLASSES, _WM_PROPERTIES)