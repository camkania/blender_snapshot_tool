import bpy
from .utils import get_scene_start, get_scene_end

class SnapshotToolProperties(bpy.types.PropertyGroup):
    frame_start: bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame for snapshots",
        default=0,
        min=0
    )
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        description="End frame for snapshots",
        default=90,
        min=1
    )
    frame_interval: bpy.props.IntProperty(
        name="Frame Interval",
        description="Interval between frames for snapshots",
        default=1
    )
    snapshot_created: bpy.props.BoolProperty(
        name="Snapshot Created",
        description="Tracks if the snapshot has been created",
        default=False
        )

class SNAPSHOT_PT_main_panel(bpy.types.Panel):
    bl_label = "Snapshot Tool"
    bl_idname = "SNAPSHOT_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Snapshot'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        snapshot_tool = scene.snapshot_tool
        

        # Save/Load Object Set
        #layout.operator("snapshot.save_objects", text="Save Object Set")
        #layout.operator("snapshot.load_objects", text="Load Object Set")

        # Frame Range Input
        layout.prop(snapshot_tool, "frame_start")
        layout.prop(snapshot_tool, "frame_end")

        # Interval Input
        layout.prop(snapshot_tool, "frame_interval")

        # Run the program
        layout.operator("snapshot.run_snapshots", text="Run Snapshot Process")

        # Combine meshes
        combined_op = layout.operator("snapshot.combine_meshes", text="Combine Snapshots into Mesh")
        combined_op.enabled = snapshot_tool.snapshot_created


# Registering the custom properties and UI panel
def register_ui():
    bpy.utils.register_class(SNAPSHOT_PT_main_panel)
    bpy.utils.register_class(SnapshotToolProperties)
    bpy.types.Scene.snapshot_tool = bpy.props.PointerProperty(type=SnapshotToolProperties)


def unregister_ui():
    bpy.utils.unregister_class(SNAPSHOT_PT_main_panel)
    bpy.utils.unregister_class(SnapshotToolProperties)
    del bpy.types.Scene.snapshot_tool
