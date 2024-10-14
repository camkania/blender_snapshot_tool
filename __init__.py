bl_info = {
    "name": "Snapshot",
    "description": "Store a static mesh copy of the selected objects at a given frame interval",
    "author": "@Camkania",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": 'VIEW_3D',
    "doc_url": "https://github.com/camkania/blender_snapshot_tool/blob/main/README.md",
    "tracker_url": "https://github.com/camkania/blender_snapshot_tool/issues",
    "Support": "COMMUNITY",
    "category": "Add Mesh",  
}

from .operators import *
from .ui import *

def register():
    # Register your operators and panels here
    pass

def unregister():
    # Unregister your operators and panels here
    pass
