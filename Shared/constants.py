# -*- coding: utf-8 -*-

import bpy  # type: ignore

from enum   import Enum

# Links
EXTERNAL_DL_URL     = "https://apps.microsoft.com/detail/9n6lbd4t985r?hl=de-DE&gl=DE"
EXTERNAL_WB_URL     = "https://www.bleqapp.eu/"
EXTERNAL_WB_GIT     = "https://github.com/CMcKarskiCNC/BLeQ"
EXTERNAL_MAIL_SUP   = "mailto:BLeQ@mail.gmx"

# blender version
BLENDERVER = bpy.app.version

# Debug Mode
DEBUG_MODE = True

# Preview Collection for Icons
PREVIEW_COLLECTION  = {}
COLL_ID             = "main"
ICONPATH            = "icons"


#reg helper functions
def regfunction(util_classes = None, wm_properties = None):
    # util classes
    if util_classes:
        for cls in util_classes:
            bpy.utils.register_class(cls)

    # wm properties
    if wm_properties:
        for prop in wm_properties:
            prop_name = prop["name"]
            # message
            if not hasattr(bpy.types.WindowManager, prop_name):
                print(f"register Property / BLeQSender / operator: {prop_name} is already registered. Will be overwritten")

            if prop["type"] == "collection":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.CollectionProperty(type=prop["prop_type"]))
            elif prop["type"] == "int":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.IntProperty(
                    name        =prop.get("UI_Name", "None"),
                    default     =prop.get("default", 0),
                    description =prop.get("description", "")))
            elif prop["type"] == "bool":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.BoolProperty(
                    name        =prop.get("UI_Name", "None"),
                    default     =prop.get("default", False),
                    description =prop.get("description", "")))
            elif prop["type"] == "float":
                setattr(bpy.types.WindowManager, prop_name, bpy.props.FloatProperty(
                    name        =prop.get("UI_Name", "None"),
                    default     =prop.get("default", 0.0),
                    min         =prop.get("min", 0.0),
                    max         =prop.get("max", 100.0),
                    subtype     =prop.get("subtype", "NONE"),
                    description =prop.get("description", "")))

def unregfunction(util_classes = None, wm_properties = None):
    # Remove properties
    if wm_properties:
        for prop in reversed(wm_properties):
            prop_name = prop["name"]
            delattr(bpy.types.WindowManager, prop_name)
    
    # Unregister classes
    if util_classes:
        for cls in reversed(util_classes):
            bpy.utils.unregister_class(cls)


# imageintegraten
class images(str, Enum):
    BLEQ_ICON = "BLeQ_ICON"

def get_icon(icon_name: images):
    pcoll = PREVIEW_COLLECTION.get(COLL_ID)
    if pcoll and icon_name in pcoll:
        return pcoll[icon_name].icon_id
    return 0
