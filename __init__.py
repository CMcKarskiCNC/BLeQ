# -*- coding: utf-8 -*-

bl_info = {
    "name":         "BLeQ",
    "author":       "CMckarski",
    "version":      (1, 0, 3),
    "blender":      (4, 2, 0),
    "location":     "View3D > Sidebar > External Tool",
    "description":  "Renderqueue / 3DHomePageCreator / Hardwaremonitor / Tools",
    "category":     "System",
    "license":      "GPL-3.0-or-later",
}

from .Shared        import constants    as const
from .BleQSetup     import operators    as setup_operators
from .BLeQSender    import operators    as sender_operators
from .BLeQSender    import BLeQSender   as bleq_sender
from .Shared        import panels
from .Shared        import logger       as log

_MODULES = (
    setup_operators,
    sender_operators,
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