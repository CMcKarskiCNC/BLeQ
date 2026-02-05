# -*- coding: utf-8 -*-

import bpy          # type: ignore
import webbrowser

from ..Shared   import constants    as const
from ..Shared   import logger       as log

class BLEQ_OT_open_dllink(bpy.types.Operator):
    bl_idname       = "external.open_bleq_dllink"
    bl_label        = "BLeQ DownLoad Page"
    bl_description  = "Open the download website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_DL_URL)
        return {'FINISHED'}

class BLEQ_OT_open_website(bpy.types.Operator):
    bl_idname       = "external.open_bleq_website"
    bl_label        = "BLeQ HomePage"
    bl_description  = "Open the BLeQ website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_WB_URL)
        return {'FINISHED'}

class BLEQ_OT_open_git(bpy.types.Operator):
    bl_idname       = "external.open_git_website"
    bl_label        = "BLeQ on GIT"
    bl_description  = "Open the BLeQ website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_WB_GIT)
        return {'FINISHED'}

class BLEQ_OT_mail(bpy.types.Operator):
    bl_idname       = "external.open_support_email"
    bl_label        = "Contact support"
    bl_description  = "Open the BLeQ website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_MAIL_SUP)
        return {'FINISHED'}

# register grouping
_UTIL_CLASSES =(
    BLEQ_OT_open_dllink,
    BLEQ_OT_open_website,
    BLEQ_OT_open_git,
    BLEQ_OT_mail,
)

def register():
    # classes
    for cls in _UTIL_CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_UTIL_CLASSES):
        bpy.utils.unregister_class(cls)