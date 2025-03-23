import bpy

# Set the end frame for the simulation
bpy.context.scene.frame_end = 100

# Define mass value for the cloth object (only 0.1)
mass = [0.1]

# Create the sphere and corresponding cloth plane
sph_position = 0  # Position for the single sphere
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, radius=0.5, location=(sph_position, 0, 1))
sphere = bpy.context.active_object
sphere.name = 'Sphere_0'
bpy.ops.object.shade_smooth() 
bpy.ops.object.modifier_add(type='COLLISION')

# Create a cloth plane
bpy.ops.mesh.primitive_plane_add(size=2.8, location=(sph_position, 0, 3))
plane = bpy.context.active_object
plane.name = 'myCloth_0'

# Subdivide the plane
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=50)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

# Add cloth modifier
bpy.ops.object.modifier_add(type='CLOTH')
cloth_mod = plane.modifiers["Cloth"]
cloth_mod.settings.quality = 10
cloth_mod.settings.mass = mass[0]
cloth_mod.point_cache.frame_end = 100
cloth_mod.collision_settings.collision_quality = 5
cloth_mod.collision_settings.use_self_collision = True

# Add Subdivision and Solidify modifiers to the cloth
cloth_obj = bpy.data.objects['myCloth_0']
bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
bpy.context.view_layer.objects.active = cloth_obj  # Set the cloth as the active object
cloth_obj.select_set(True)

# Add Subdivision modifier
bpy.ops.object.modifier_add(type='SUBSURF')
subdiv_mod = cloth_obj.modifiers["Subdivision"]
subdiv_mod.levels = 3
subdiv_mod.render_levels = 3

# Add Solidify modifier
bpy.ops.object.modifier_add(type='SOLIDIFY')
solidify_mod = cloth_obj.modifiers["Solidify"]
solidify_mod.thickness = 0.03

# Optional: Bake physics if required
# bpy.ops.ptcache.bake_all(bake=True)
