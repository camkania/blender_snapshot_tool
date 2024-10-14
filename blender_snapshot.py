import bpy
import bmesh
from mathutils import Matrix
import time 

def create_snapshot_collection(base_name):
    collection_name = f"{base_name}"
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    return bpy.data.collections[collection_name]

def create_mesh_snapshot(obj, frame):
    new_mesh = bpy.data.meshes.new(name=f"{obj.name}_Frame_{frame}_Mesh")
    bm = bmesh.new()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    
    # Get the world matrix of the evaluated object
    world_matrix = eval_obj.matrix_world
    
    # Create a bmesh from the evaluated object
    bm.from_object(eval_obj, depsgraph)
    
    # Transform the bmesh vertices to world space
    bmesh.ops.transform(bm, matrix=world_matrix, verts=bm.verts)
    
    bm.to_mesh(new_mesh)
    bm.free()
    new_mesh.update()
    return new_mesh

def set_active_collection(layer_collection, collection_name):
    if layer_collection.name == collection_name:
        bpy.context.view_layer.active_layer_collection = layer_collection
        return True
    for child in layer_collection.children:
        if set_active_collection(child, collection_name):
            return True
    return False

def get_selected_objects():
    return [obj.name for obj in bpy.context.selected_objects if obj.type == 'MESH']

def create_snapshots(obj_names):
    start_time = time.time()
    snapshot_collection = create_snapshot_collection("Snapshot")
    
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        
        for obj_name in obj_names:
            if obj_name in bpy.data.objects:
                obj = bpy.data.objects[obj_name]
                new_mesh = create_mesh_snapshot(obj, frame)
                new_obj = bpy.data.objects.new(f"{obj_name}_Frame_{frame}", new_mesh)
                snapshot_collection.objects.link(new_obj)
                
                # Set the new object's transform to identity
                new_obj.matrix_world = Matrix.Identity(4)
            else:
                print(f"Warning: Object '{obj_name}' not found in the scene.")
    
    layer_collection = bpy.context.view_layer.layer_collection
    set_active_collection(layer_collection, snapshot_collection.name)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("Snapshot creation complete!")
    print(f"Execution time: {elapsed_time:.2f} seconds")

# Add the meshes you want to this list
object_names = [
"axis1_geo", 
"axis2_geo", 
"axis2_piston_left",
"axis2_piston_right",
"axis2_pistonRod_left",
"axis2_pistonRod_right",
"axis3_geo",
"axis3_cabling",
"axis4_geo",
"axis4_cabling",
"axis5_geo",
"axis6_geo",
"base",
"counterWeight",
"counterWeight_arm"
]

selected_object_names = get_selected_objects()

if selected_object_names:
    print(f"Selected objects: {', '.join(selected_object_names)}")
    create_snapshots(selected_object_names)
else:
    print("No mesh objects selected. Please select one or more mesh objects and run the script again.")

#create_snapshots(object_names)
