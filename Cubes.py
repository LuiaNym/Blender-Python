import bpy
import random


def create_random_colored_cube(x, y, frame_start=1, frame_end=120, frame_steps=5):  
    # Randomly select the initial Z position
    z_initial = random.uniform(0, 0.8)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z_initial + 0.5))
    cube = bpy.context.object

    # Create a random color 
    r = random.uniform(0.0, 0.5)  # Red 
    g = random.uniform(0.0, 0.2)  # Green is now limited to a maximum of 0.2
    b = random.uniform(0.0, 0.5)  # Blue 

    # Create and apply the material
    color = (r, g, b, 1)
    mat = bpy.data.materials.new(name="RandomMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    cube.data.materials.append(mat)

    # Add and apply modifiers (Bevel and Subdivision Surface)
    for mod_type, params in [("BEVEL", {"width": 0.11, "segments": 3}), ("SUBSURF", {"levels": 3, "render_levels": 3})]:
        bpy.ops.object.modifier_add(type=mod_type)
        mod = cube.modifiers[-1]
        for key, value in params.items():
            setattr(mod, key, value)
        bpy.ops.object.modifier_apply(modifier=mod.name)
        

    # Insert the initial Z position as a keyframe
    cube.location.z = z_initial
    cube.keyframe_insert(data_path="location", frame=frame_start, index=2)

    # Create animation steps (random Z movement)
    frame_interval = (frame_end - frame_start) / (frame_steps + 1)
    for i in range(1, frame_steps + 1):
        z_random_move = random.uniform(0, 0.8)
        frame = frame_start + i * frame_interval
        cube.location.z = z_random_move
        cube.keyframe_insert(data_path="location", frame=frame, index=2)

def create_grid():
    # Grid size and spacing
    grid_size, spacing = 20, 1.0
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)  # Delete old objects

    # Create the grid and place the cubes
    for i in range(grid_size):
        for j in range(grid_size):
            create_random_colored_cube((i - grid_size // 2) * spacing, (j - grid_size // 2) * spacing)

# Create the grid
create_grid()
