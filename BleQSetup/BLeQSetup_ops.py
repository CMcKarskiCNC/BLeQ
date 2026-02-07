# -*- coding: utf-8 -*-

import bpy          # type: ignore
import webbrowser

from ..Shared   import constants    as const


class BLEQ_OT_tutorial_website(bpy.types.Operator):
    bl_idname       = "bleq.open_bleq_tutorial"
    bl_label        = "BLeQ Tutorial (coming soon)"
    bl_description  = "Open the BLeQ tutorial website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_WB_URL)
        return {'FINISHED'}

class BLEQ_OT_open_git(bpy.types.Operator):
    bl_idname       = "bleq.open_git_website"
    bl_label        = "BLeQ on GIT"
    bl_description  = "Open the BLeQ website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_WB_GIT)
        return {'FINISHED'}

class BLEQ_OT_mail(bpy.types.Operator):
    bl_idname       = "bleq.open_support_email"
    bl_label        = "Contact support"
    bl_description  = "Open the BLeQ website in your browser"

    def execute(self, context):
        webbrowser.open(const.EXTERNAL_MAIL_SUP)
        return {'FINISHED'}

# register grouping
_UTIL_CLASSES =(
    BLEQ_OT_tutorial_website,
    BLEQ_OT_open_git,
    BLEQ_OT_mail,
)

def register():
    const.regfunction(_UTIL_CLASSES)

def unregister():
    const.unregfunction(_UTIL_CLASSES)