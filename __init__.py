# -*- coding: utf-8 -*-

bl_info = {
    "name":         "BLeQ",
    "author":       "CMckarski",
    "version":      (1, 0, 5),
    "blender":      (4, 2, 0),
    "location":     "View3D > Sidebar > External Tool",
    "description":  "Renderqueue / 3DHomePageCreator / Hardwaremonitor / Tools",
    "category":     "System",
    "license":      "GPL-3.0-or-later",
}

import bpy # type: ignore

from .Shared        import panels

from .BleQSetup     import BLeQSetup_ops    as setup_operators

from .BLeQSender    import BLeQSender_ops   as sender_operators
from .BLeQSender    import BLeQSender       as bleq_sender

from .BLonitor      import BLonitor         as blonitor


_MODULES = (
    setup_operators,
    sender_operators,
    blonitor,
    bleq_sender,
    panels,
)

def register():
    for m in _MODULES:
        m.register()

def unregister():
    for m in reversed(_MODULES):
        m.unregister()

if __name__ == "__main__":
    register()