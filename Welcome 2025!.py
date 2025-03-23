import bpy
import random
import math

# Snowflake 

snowflake = bpy.data.objects.get("Snowflake")
if snowflake:
    for _ in range(180):
        new_snowflake = snowflake.copy()
        new_snowflake.data = snowflake.data.copy()
        bpy.context.collection.objects.link(new_snowflake)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(1, 3)
        new_snowflake.location = (math.cos(angle) * radius, math.sin(angle) * radius, random.uniform(-1, 4))
        new_snowflake.rotation_euler = (random.uniform(-1, 1), random.uniform(-1,1), random.uniform(-1, 1))
        scale_factor = 0.5  
        new_snowflake.scale = (scale_factor, scale_factor, scale_factor)
       
        if not new_snowflake.rigid_body:
            bpy.context.view_layer.objects.active = new_snowflake  
            bpy.ops.rigidbody.object_add()  
        new_snowflake.rigid_body.type = 'ACTIVE'
        new_snowflake.rigid_body.mass = 0.06
        new_snowflake.rigid_body.friction = 0.5
        new_snowflake.rigid_body.restitution = 0.3

        material = bpy.data.materials.new(name="SnowflakeMaterial")
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
        bsdf.inputs["Roughness"].default_value = 0.1
        emission = material.node_tree.nodes.new(type='ShaderNodeEmission')
        emission.inputs["Color"].default_value = (1, 1, 1, 1)
        emission.inputs["Strength"].default_value = 30
        material.node_tree.links.new(emission.outputs["Emission"], material.node_tree.nodes["Material Output"].inputs["Surface"])
        new_snowflake.data.materials.append(material)
    print("Successfully created 100 Snowflake objects.")
else:
    print("Snowflake object not found.")

# 2025 

numbers = ['2', '0', '2', '5']
for i, num in enumerate(numbers):
    bpy.ops.object.text_add(location=(0, i * 0.5 - 1, 2))
    text_obj = bpy.context.active_object
    text_obj.data.body = num  
    text_obj.rotation_euler = (math.radians(90), 0, math.radians(90))  
    bpy.ops.object.convert(target='MESH')
    text_obj.scale = (0.8, 0.8, 0.8)

    material = bpy.data.materials.new(name=f"Material_{num}")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.2, 0, 0, 1)  
    text_obj.data.materials.append(material)

    solidify = text_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.18  

    if not text_obj.rigid_body:
        bpy.context.view_layer.objects.active = text_obj  
        bpy.ops.rigidbody.object_add()  
        text_obj.rigid_body.type = 'ACTIVE'  
        text_obj.rigid_body.mass = 0.1  
        text_obj.rigid_body.friction = 0.8  
        text_obj.rigid_body.restitution = 0.3  

print("Successfully placed the 2025 digits and applied Rigid Body Active.")

# Plane

plane = bpy.data.objects.get("Plane")
if plane:
    bpy.context.view_layer.objects.active = plane
    if not plane.rigid_body:
        bpy.ops.rigidbody.object_add() 
    plane.rigid_body.type = 'PASSIVE'  
    plane.rigid_body.friction = 0.5    
    print("Successfully applied Rigid Body Passive to the Plane object.")
else:
    print("Plane object not found.")
    
# Wind & Turbulence    

def add_force_field(type, name, strength, flow, direction=None, deviation=None, size=None, noise=None):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(2, 0, 0))  
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.forcefield_toggle()  
    obj.field.type = type
    obj.field.strength = strength
    obj.field.flow = flow
    if direction: obj.field.direction = direction
    if deviation: obj.field.deviation = deviation
    if size: obj.field.size = size
    if noise: obj.field.noise = noise
    obj.field.gravity = 0  

add_force_field('WIND', 'Wind', 10, 1, direction=(1, 0, 0), deviation=5)
add_force_field('TURBULENCE', 'Turbulence', 5, 1, size=1, noise=0.5)

print("Successfully added Wind and Turbulence effects.")
