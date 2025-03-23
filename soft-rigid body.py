import bpy
import random
import math


### GROUND ###

def create_ground():
     # Create ground plane
    bpy.ops.mesh.primitive_cube_add(size=66, location=(10, 0, 0))
    ground = bpy.context.object
    ground.name = 'Ground'
    ground.scale.z = 0.02  # Ground thickness
    
    # Add collision modifier
    bpy.ops.object.modifier_add(type='COLLISION')
    
    # Create metallic material
    ground_material = bpy.data.materials.new(name="SilverMetalMaterial")
    ground_material.use_nodes = True
    nodes = ground_material.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    if principled_bsdf:
        principled_bsdf.inputs['Base Color'].default_value = (0.75, 0.75, 0.75, 1)  # Silver color
        principled_bsdf.inputs['Metallic'].default_value = 1
        principled_bsdf.inputs['Roughness'].default_value = 0.2

    # Assign material
    if ground.data.materials:
        ground.data.materials[0] = ground_material
    else:
        ground.data.materials.append(ground_material)
    
    # Add rigid body as passive
    #bpy.ops.rigidbody.object_add()
    #ground.rigid_body.type = 'PASSIVE'
    #ground.rigid_body.friction = 1.0
    #return ground


### OBJECT CREATION ###

def create_objects(num_objects=28, radius=1, min_distance=3.6):
    """Creates objects with random positions, softbody physics, and dynamic behaviors."""
    occupied_positions = []  # Track placed positions
    
    def is_position_valid(position):
        """Checks if a position is far enough from existing objects."""
        for existing_position in occupied_positions:
            if math.dist(position, existing_position) < min_distance:
                return False
        return True

    for _ in range(num_objects):
        # Generate a random position
        while True:
            new_position = (
                random.uniform(-10, 10),  # Random X
                random.uniform(-10, 10),  # Random Y
                random.uniform(5, 15)    # Random Z
            )
            if is_position_valid(new_position):
                break
        
        occupied_positions.append(new_position)
        

        # Create icosphere
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=radius, location=new_position)
        obj = bpy.context.object
        
        
        # Enable smooth shading
        bpy.ops.object.shade_smooth()
            
        # Unwrap the object to avoid UV issues with soft body :(
        
                    
        # Assign material if available
        material = bpy.data.materials.get("Stripe_Material")
        if material:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
        else:
            print("Material not found: Stripe_Material")
                

        # Add random rotation
        obj.rotation_euler = (
            random.uniform(0, math.pi), 
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        )

        # Add random scale
        scale_factor = random.uniform(0.8, 1.8)
        obj.scale = (scale_factor, scale_factor, scale_factor)

        # Add rigid body physics
        #bpy.ops.rigidbody.object_add()
        #obj.rigid_body.type = 'ACTIVE'
        #obj.rigid_body.mass = random.uniform(0.5, 3)
        #obj.rigid_body.friction = 0.5
        #obj.rigid_body.restitution = 0.8
        

        # Add softbody physics
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_add(type='SOFT_BODY')
        bpy.context.object.modifiers["Softbody"].settings.friction = 0.1
        bpy.context.object.modifiers["Softbody"].settings.use_goal = False
        bpy.context.object.modifiers["Softbody"].settings.use_self_collision = True
        bpy.context.object.modifiers["Softbody"].settings.use_stiff_quads = True
        bpy.context.object.modifiers["Softbody"].settings.pull = 0.8
        bpy.context.object.modifiers["Softbody"].settings.push = 0.8
        bpy.context.object.modifiers["Softbody"].settings.damping = 0.9
        bpy.context.object.modifiers["Softbody"].settings.shear = 0.9
        bpy.context.object.modifiers["Softbody"].settings.bend = 0.9 
        bpy.context.object.modifiers["Softbody"].settings.mass = 0.11
        bpy.ops.object.modifier_add(type='COLLISION')
        
        


### MAIN EXECUTION ###
# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create ground and objects
create_ground()
create_objects(num_objects=28)
