import bpy
import bmesh
from .utils import get_selected_objects, create_snapshots

'''
# Operator to save object set
class SNAPSHOT_OT_save_objects(bpy.types.Operator):
    bl_label = "Save Object Set"
    bl_idname = "snapshot.save_objects"
    
    def execute(self, context):
        obj_names = get_selected_objects()
        context.scene['saved_objects'] = obj_names
        self.report({'INFO'}, "Objects saved.")
        return {'FINISHED'}

class SNAPSHOT_OT_load_objects(bpy.types.Operator):
    bl_label = "Load Object Set"
    bl_idname = "snapshot.load_objects"

    def execute(self, context):
        obj_names = context.scene.get('saved_objects', [])
        if not obj_names:
            self.report({'WARNING'}, "No saved objects found.")
            return {'CANCELLED'}
        for obj_name in obj_names:
            if obj_name in bpy.data.objects:
                obj = bpy.data.objects[obj_name]
                obj.select_set(True)
        self.report({'INFO'}, "Objects loaded.")
        return {'FINISHED'}

'''

class SNAPSHOT_OT_run_snapshots(bpy.types.Operator):
    bl_label = "Run Snapshot Process"
    bl_idname = "snapshot.run_snapshots"

    def execute(self, context):
        tool = context.scene.snapshot_tool
        obj_names = get_selected_objects()

        for frame in range(tool.frame_start, tool.frame_end + 1, tool.frame_interval):
            bpy.context.scene.frame_set(frame)
            create_snapshots(obj_names)
        
        self.report({'INFO'}, "Snapshots completed.")
        return {'FINISHED'}


class SNAPSHOT_OT_combine_meshes(bpy.types.Operator):
    bl_label = "Combine Snapshots into Mesh"
    bl_idname = "snapshot.combine_meshes"

    def execute(self, context):
        snapshot_collection = create_snapshot_collection("Snapshot")
        combined_mesh = bpy.data.meshes.new(name="Combined_Mesh")
        bm_combined = bmesh.new()

        for obj in snapshot_collection.objects:
            if obj.type == 'MESH':
                bm_temp = bmesh.new()
                bm_temp.from_mesh(obj.data)
                bm_combined.from_mesh(obj.data)
                bm_temp.free()

        bm_combined.to_mesh(combined_mesh)
        new_obj = bpy.data.objects.new("Combined_Snapshot", combined_mesh)
        context.scene.collection.objects.link(new_obj)
        bm_combined.free()

        self.report({'INFO'}, "Meshes combined.")
        return {'FINISHED'}



# Register and unregister functions
classes = [
    #SNAPSHOT_OT_save_objects,
    #SNAPSHOT_OT_load_objects,
    SNAPSHOT_OT_run_snapshots,
    SNAPSHOT_OT_combine_meshes
]

def register_operators():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_operators():
    for cls in classes:
        bpy.utils.unregister_class(cls)