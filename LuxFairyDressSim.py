import bpy


bpy.context.scene.frame_end = 100

mass = [0.15]

# Load or select your dress object
if 'Dress' in bpy.data.objects:
    dress_obj = bpy.data.objects['Dress']  # Change this to your dress object's name
else:
    raise ValueError("Object 'Dress' not found in the scene.")

# Load or select your body object
if 'Body' in bpy.data.objects:
    body_obj = bpy.data.objects['Body']  # Change this to your body object's name
else:
    raise ValueError("Object 'Body' not found in the scene.")

# Make sure the Dress object is selected and active
bpy.context.view_layer.objects.active = dress_obj
dress_obj.select_set(True)

# Optional: Apply all transformations to ensure the object is correctly scaled and positioned
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


# Add Cloth modifier to Dress
bpy.ops.object.modifier_add(type='CLOTH')
cloth_mod = dress_obj.modifiers["Cloth"]
cloth_mod.settings.quality = 10
cloth_mod.settings.mass = mass[0]
cloth_mod.point_cache.frame_end = 100
cloth_mod.collision_settings.collision_quality = 5
cloth_mod.collision_settings.use_self_collision = True

cloth_mod.settings.tension_stiffness = 5
cloth_mod.settings.compression_stiffness = 5
cloth_mod.settings.shear_stiffness = 1
cloth_mod.settings.bending_stiffness = 0.1
cloth_mod.settings.air_damping = 3

# Add Subdivision modifier
bpy.ops.object.modifier_add(type='SUBSURF')
subdiv_mod = dress_obj.modifiers["Subdivision"]
subdiv_mod.levels = 1
subdiv_mod.render_levels = 1

# Add Solidify modifier
#bpy.ops.object.modifier_add(type='SOLIDIFY')
#solidify_mod = dress_obj.modifiers["Solidify"]
#solidify_mod.thickness = 0.03

# Add Collision modifier to Body
bpy.context.view_layer.objects.active = body_obj
body_obj.select_set(True)
bpy.ops.object.modifier_add(type='COLLISION')
collision_mod = body_obj.modifiers["Collision"]
collision_mod.settings.damping = 0.5
collision_mod.settings.thickness_outer = 0.02
collision_mod.settings.thickness_inner = 0.015
collision_mod.settings.friction = 5.0


# Bake all physics simulations
bpy.ops.ptcache.free_bake_all()  # Clear previous cache
bpy.ops.ptcache.bake_all(bake=True)  # Bake the simulations
