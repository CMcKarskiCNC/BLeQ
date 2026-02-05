# -*- coding: utf-8 -*-

import bpy  # type: ignore

from ..Shared   import logger       as log
from .          import operators    as ops

# Module-level state for handler access
_queue_state = {
    "is_rendering": False,
    "operator":     None,
    "stopped":      False,
}

# event handlers
def _on_render_complete(scene):
    _queue_state["is_rendering"] = False

def _on_render_cancel(scene):
    _queue_state["stopped"]         = True
    _queue_state["is_rendering"]    = False

def _on_list_Update():
    wm = bpy.context.window_manager
    if not wm.bleq_queue_running:
        return


# render queue control functions
def start_queue_render():
    bpy.ops.render.bleq_queue_render('INVOKE_DEFAULT')

def stop_queue_render():
    print("Stopping BLeQ render queue...")

def add_queue_file():
    wm                  = bpy.context.window_manager
    idx                 = wm.bleq_string_list_index
    item                = wm.bleq_string_list.add()
    item.filepath       = bpy.data.filepath
    item.scene_name     = bpy.context.scene.name           if bpy.context.scene else "None"
    item.camera_name    = bpy.context.scene.camera.name    if bpy.context.scene and bpy.context.scene.camera else "None"
    item.name           = f"{bpy.path.display_name_from_filepath(bpy.data.filepath)}"

    new_idx             = len(wm.bleq_string_list) - 1
    target_idx          = min(idx + 1, new_idx)
    wm.bleq_string_list.move(new_idx, target_idx)
    wm.bleq_string_list_index = target_idx

def add_queue_file_last():
    wm                          = bpy.context.window_manager
    item                        = wm.bleq_string_list.add()
    item.filepath               = bpy.data.filepath
    item.scene_name             = bpy.context.scene.name           if bpy.context.scene else "None"
    item.camera_name            = bpy.context.scene.camera.name    if bpy.context.scene and bpy.context.scene.camera else "None"
    item.name                   = f"{bpy.path.display_name_from_filepath(bpy.data.filepath)}"
    wm.bleq_string_list_index   = len(wm.bleq_string_list) - 1

def add_queue_all_scenes():
    wm = bpy.context.window_manager
    for scene in bpy.data.scenes:
        item                    = wm.bleq_string_list.add()
        item.filepath           = bpy.data.filepath
        item.scene_name         = scene.name
        item.camera_name        = scene.camera.name if scene.camera else "None"
        item.name               = f"{bpy.path.display_name_from_filepath(bpy.data.filepath)}"
    wm.bleq_string_list_index   = 0

def remove_queue_files():
    wm = bpy.context.window_manager
    wm.bleq_string_list.clear()
    wm.bleq_string_list_index = 0

def remove_selected_queue_file():
    wm  = bpy.context.window_manager
    idx = wm.bleq_string_list_index
    if 0 <= idx < len(wm.bleq_string_list):
        wm.bleq_string_list.remove(idx)
        wm.bleq_string_list_index = min(idx, len(wm.bleq_string_list) - 1)


# render queue operator
class BLEQ_OT_queue_render(bpy.types.Operator):
    bl_idname       = "render.bleq_queue_render"
    bl_label        = "BLeQ Queue Render"
    bl_description  = "Render queue items sequentially (ESC or Stop to cancel)"
    
    _timer          = None
    _current_index  = 0
    _iterateIndex   = False
 
    def modal(self, context, event):
        wm = context.window_manager
        
        # Cancel Rendering
        if event.type == 'ESC' or wm.bleq_stop_requested:
            self.cancel(context)
            log.logger.add(log.LogStatus.WARNING, "Queue rendering cancelled by user.")
            log.logger.print_log(self) 
            return {'CANCELLED'}
        
        # Wait until render is done
        if _queue_state["is_rendering"]:
            return {'PASS_THROUGH'}
        
        # Iterate queue
        if not _queue_state["stopped"]:
            if (not self._iterateIndex and self._current_index < len(wm.bleq_string_list)) or (self._iterateIndex and self._current_index < len(wm.bleq_string_list) - 1):
                if self._iterateIndex:
                    self._current_index         += 1
                    wm.bleq_string_list_index   += 1
                item = wm.bleq_string_list[self._current_index]
                self._iterateIndex = True
                
                # Skip if file is not the current one
                if bpy.data.filepath != item.filepath:
                    return {'RUNNING_MODAL'}
                
                # Set scene
                if item.scene_name and item.scene_name != "None":
                    if item.scene_name in bpy.data.scenes:
                        context.window.scene = bpy.data.scenes[item.scene_name]
                    else:
                        log.logger.add(log.LogStatus.WARNING, f"Scene '{item.scene_name}' not found, skipping.")
                        log.logger.print_log(self)
                        return {'RUNNING_MODAL'}
                
                # Set camera
                if item.camera_name and item.camera_name != "None":
                    if item.camera_name in context.scene.objects:
                        camera_obj = context.scene.objects[item.camera_name]
                        if camera_obj.type == 'CAMERA':
                            context.scene.camera = camera_obj
                        else:
                            return {'RUNNING_MODAL'}
                    else:
                        log.logger.add(log.LogStatus.WARNING, f"Camera '{item.camera_name}' not found in scene '{context.scene.name}', skipping.")
                        return {'RUNNING_MODAL'}
                
                log.logger.add(log.LogStatus.SUCCESS, f"Rendering {self._current_index + 1}/{len(wm.bleq_string_list)}: {item.scene_name}/{item.camera_name}")
                log.logger.print_log(self)

                _queue_state["is_rendering"] = True
                
                # Use write_still=False for animation, call synchronously
                bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
                
                return {'RUNNING_MODAL'}
        
        self.cancel(context)
        log.logger.add(log.LogStatus.SUCCESS, "Queue rendering completed.")
        return {'FINISHED'}
    
    def execute(self, context):
        wm = context.window_manager
        
        if not hasattr(wm, "bleq_string_list") or len(wm.bleq_string_list) == 0:
            log.logger.add(log.LogStatus.WARNING, "Render queue is empty.")
            log.logger.print_log(self)
            return {'CANCELLED'}
        
        self._current_index             = wm.bleq_string_list_index
        _queue_state["stopped"]         = False
        _queue_state["is_rendering"]    = False
        _queue_state["operator"]        = self
        self._iterateIndex              = False
        wm.bleq_queue_running           = True
        wm.bleq_stop_requested          = False
        
        # Timer for modal
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        
        # Register module-level handlers
        if _on_render_complete not in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.append(_on_render_complete)
        if _on_render_cancel not in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.append(_on_render_cancel)

        log.logger.add(log.LogStatus.SUCCESS, "Render started.")
        log.logger.print_log(self)      
        return {'RUNNING_MODAL'}
 
    def cancel(self, context):
        wm = context.window_manager

        wm.bleq_stop_requested          = True
        wm.bleq_queue_running           = False
        _queue_state["stopped"]         = True
        _queue_state["operator"]        = None
        _queue_state["is_rendering"]    = False

        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None  
                
        # Remove handlers
        if _on_render_complete in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(_on_render_complete)
        if _on_render_cancel in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.remove(_on_render_cancel)
        
        log.logger.print_log(self)      
        return {'FINISHED'}

# register grouping
_UTIL_CLASSES =(
    BLEQ_OT_queue_render,
)

_WM_PROPERTIES =(
    {
        "name":         "bleq_stop_requested",
        "type":         "bool",
        "description":  "BleQSender stop requested"
    },
    {
        "name":         "bleq_queue_running",
        "type":         "bool",
        "description":  "BLeQSender is running"
    },
)

def register():
    # classes
    for cls in _UTIL_CLASSES:
        bpy.utils.register_class(cls)

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