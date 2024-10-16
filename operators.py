import bpy
import bmesh
from .utils import *
import time

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
        start_time = time.time()

        tool = context.scene.snapshot_tool
        obj_names = get_selected_objects()

        for frame in range(tool.frame_start, tool.frame_end + 1, tool.frame_interval):
            bpy.context.scene.frame_set(frame)
            create_snapshots(obj_names, frame)
        
        tool.snapshot_created = True       
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.2f} seconds")
        self.report({'INFO'}, "Snapshots completed.")
        return {'FINISHED'}


class SNAPSHOT_OT_combine_meshes(bpy.types.Operator):
    bl_label = "Combine Snapshots into Mesh"
    bl_idname = "snapshot.combine_meshes"

    @classmethod
    def poll(cls, context):
        return context.scene.snapshot_tool.snapshot_created


    def execute(self, context):
        tool = context.scene.snapshot_tool
        new_obj, message = combine_snapshots(keep_separated_meshes=tool.keep_separated_meshes)
        
        if new_obj is None:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        
        self.report({'INFO'}, message)
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