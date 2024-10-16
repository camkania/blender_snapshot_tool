import bpy
import bmesh
from mathutils import Matrix 

def get_scene_start():
    return bpy.context.scene.frame_start

def get_scene_end():
    return bpy.context.scene.frame_end
    
def get_selected_objects():
    return [obj.name for obj in bpy.context.selected_objects if obj.type == 'MESH']

def create_snapshots(obj_names, frame):
    snapshot_collection = create_snapshot_collection("Snapshot_Meshes")
        
    for obj_name in obj_names:
        if obj_name in bpy.data.objects:
            obj = bpy.data.objects[obj_name]
            new_mesh = create_mesh(obj, frame)
            new_obj = bpy.data.objects.new(f"{obj_name}_Frame_{frame}", new_mesh)
            snapshot_collection.objects.link(new_obj)
            
            # Set the new object's transform to identity
            new_obj.matrix_world = Matrix.Identity(4)
        else:
            print(f"Warning: Object '{obj_name}' not found in the scene.")
    
    layer_collection = bpy.context.view_layer.layer_collection
    set_active_collection(layer_collection, snapshot_collection.name)
    

def create_snapshot_collection(base_name):
    collection_name = f"{base_name}"
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    return bpy.data.collections[collection_name]

def create_mesh(obj, frame):
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

def combine_snapshots(keep_originals=True):
    snapshot_collection = bpy.data.collections.get("Snapshot_Meshes")
    
    if not snapshot_collection:
        return None, "No snapshot collection found."

    combined_mesh = bpy.data.meshes.new(name="Combined_Snapshot")
    bm_combined = bmesh.new()

    for obj in snapshot_collection.objects:
        if obj.type == 'MESH':
            bm_temp = bmesh.new()
            bm_temp.from_mesh(obj.data)
            bm_temp.transform(obj.matrix_world)
            bm_combined.from_mesh(obj.data)
            bm_temp.free()

    bm_combined.to_mesh(combined_mesh)
    combined_mesh.update()
    
    new_obj = bpy.data.objects.new("Combined_Snapshot", combined_mesh)
    bpy.context.scene.collection.objects.link(new_obj)
    
    bm_combined.free()

    # Remove original snapshot objects
    if not keep_seperated_meshes:
        for obj in snapshot_collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)

    return new_obj, "Meshes combined successfully."