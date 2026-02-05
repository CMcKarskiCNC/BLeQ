# -*- coding: utf-8 -*-

import bpy  # type: ignore
import os

from enum   import Enum

# Links
EXTERNAL_DL_URL     = "https://apps.microsoft.com/detail/9n6lbd4t985r?hl=de-DE&gl=DE"
EXTERNAL_WB_URL     = "https://www.bleqapp.eu/"
EXTERNAL_WB_GIT     = "https://github.com/CMcKarskiCNC/BLeQ"
EXTERNAL_MAIL_SUP   = "mailto:BLeQ@mail.gmx"

# Debug Mode
DEBUG_MODE = True

# Preview Collection for Icons
PREVIEW_COLLECTION  = {}
COLL_ID             = "main"
ICONPATH            = "icons"

class images(str, Enum):
    BLEQ_ICON = "BLeQ_ICON"

def get_icon(icon_name: images):
    pcoll = PREVIEW_COLLECTION.get(COLL_ID)
    if pcoll and icon_name in pcoll:
        return pcoll[icon_name].icon_id
    return 0


BLENDERVER = bpy.app.version
