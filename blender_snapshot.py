import bpy

# Set the object to duplicate (replace "Cube" with the name of your object)
obj_name = "Icosphere"
obj = bpy.data.objects[obj_name]

# Range of frames to iterate over
start_frame = bpy.context.scene.frame_start
end_frame = bpy.context.scene.frame_end

# Loop through each frame
for frame in range(start_frame, end_frame + 1):
    # Set the frame
    bpy.context.scene.frame_set(frame)
    
    # Duplicate the object
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()  # Copy the mesh data
    bpy.context.collection.objects.link(new_obj)
    
    # Rename the object to include the frame number
    new_obj.name = f"{obj_name}_Frame_{frame}"
    
    # Set the location, rotation, and scale to match the current frame
    new_obj.location = obj.location.copy()
    new_obj.rotation_euler = obj.rotation_euler.copy()
    new_obj.scale = obj.scale.copy()

    # Remove any animation data from the new object
    new_obj.animation_data_clear()

print("Duplication complete!")
