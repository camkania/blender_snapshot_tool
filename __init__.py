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

import bpy
from .operators import register_operators, unregister_operators
from .ui import register_ui, unregister_ui


def register():
    bpy.utils.register_class(SnapshotToolProperties)
    bpy.types.Scene.snapshot_tool = bpy.props.PointerProperty(type=SnapshotToolProperties)
    
    register_ui()
    register_operators()

def unregister():
    unregister_ui()
    unregister_operators()
    
    del bpy.types.Scene.snapshot_tool
    bpy.utils.unregister_class(SnapshotToolProperties)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
