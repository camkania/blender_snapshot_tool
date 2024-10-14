import bpy

class SnapshotToolProperties(bpy.types.PropertyGroup):
    frame_start: bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame for snapshots",
        default=lambda: bpy.context.scene.frame_start
    )
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        description="End frame for snapshots",
        default=lambda: bpy.context.scene.frame_end
    )
    frame_interval: bpy.props.IntProperty(
        name="Frame Interval",
        description="Interval between frames for snapshots",
        default=1
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

        # Frame Range Input
        layout.prop(snapshot_tool, "frame_start")
        layout.prop(snapshot_tool, "frame_end")

        # Interval Input
        layout.prop(snapshot_tool, "frame_interval")

        # Save/Load Object Set
        #layout.operator("snapshot.save_objects", text="Save Object Set")
        #layout.operator("snapshot.load_objects", text="Load Object Set")

        # Run the program
        layout.operator("snapshot.run_snapshots", text="Run Snapshot Process")

        # Combine meshes
        layout.operator("snapshot.combine_meshes", text="Combine Snapshots into Mesh")


# Registering the custom properties and UI panel
def register_ui():
    bpy.utils.register_class(SNAPSHOT_PT_main_panel)
    bpy.utils.register_class(SnapshotToolProperties)
    bpy.types.Scene.snapshot_tool = bpy.props.PointerProperty(type=SnapshotToolProperties)


def unregister_ui():
    bpy.utils.unregister_class(SNAPSHOT_PT_main_panel)
    bpy.utils.unregister_class(SnapshotToolProperties)
    del bpy.types.Scene.snapshot_tool