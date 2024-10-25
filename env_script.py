import bpy
import math
import numpy as np

#clear any previously generated corkscrew orbit curves ===
for obj in bpy.data.objects:
    if obj.name.startswith("CorkscrewOrbit"):
        bpy.data.objects.remove(obj, do_unlink=True)

#define scaled Earth radius and orbit altitude ===
earth_radius = 6371 / 1000  # earth's radius scaled down by 1/1000 (6.371 BU)
orbit_altitude = 200 / 1000  # orbit altitude scaled down (0.2 BU)
total_orbit_radius = earth_radius + orbit_altitude  # total orbit radius

#orbit parameters
inclination = 45 * np.pi / 180  
T = 2 * np.pi * np.sqrt((total_orbit_radius ** 3) / 398600.44)  
omega = 2 * np.pi / T  #angular velocity

#generate trajectory points for the corkscrew orbit
num_points = 1000  
t = np.linspace(0, 2 * T, num_points)  

#calculate trajectory points for the corkscrew path
x_t = total_orbit_radius * np.cos(omega * t)
y_t = total_orbit_radius * np.sin(inclination) * np.sin(omega * t)
z_t = np.linspace(orbit_altitude, orbit_altitude + 0.2, num_points)  # Vertical corkscrew effect

#create curved object to represent the corkscrew orbit
curve_data = bpy.data.curves.new('CorkscrewOrbit', type='CURVE')
curve_data.dimensions = '3D'
spline = curve_data.splines.new('POLY')
spline.points.add(num_points - 1)

# assign trajectory points to the spline
for i, (x, y, z) in enumerate(zip(x_t, y_t, z_t)):
    spline.points[i].co = (x, y, z, 1)  # Homogeneous coordinates

#create and link the corkscrew path
corkscrew_path = bpy.data.objects.new('CorkscrewOrbit', curve_data)

if 'Corkscrew' not in bpy.data.collections:
    corkscrew_collection = bpy.data.collections.new('Corkscrew')
    bpy.context.scene.collection.children.link(corkscrew_collection)
else:
    corkscrew_collection = bpy.data.collections['Corkscrew']

corkscrew_collection.objects.link(corkscrew_path)

#select and scale the satellite ===
satellite = bpy.data.objects['Satellite']
satellite.scale = (0.015, 0.003, 0.003)  # Satellite scaled by 1/1000
bpy.ops.object.transform_apply(scale=True)  # Apply scaling

#add a follow path constraint to the satellite
constraint = satellite.constraints.new(type='FOLLOW_PATH')
constraint.target = corkscrew_path  
constraint.use_curve_follow = True  

#set the satellite's initial position
satellite.location = (x_t[0], y_t[0], z_t[0])

#set the path animation duration
corkscrew_path.data.path_duration = int(T)

#add keyframes for animation
constraint.offset_factor = 0  # start of path
satellite.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=1)
constraint.offset_factor = 1  # end of path
satellite.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=int(T))

#scale and center earth layers (Atmo, Clouds, Surface)
for layer_name in ['Atmo', 'Clouds', 'Surface']:
    if layer_name in bpy.data.objects:
        layer = bpy.data.objects[layer_name]
        layer.scale = (earth_radius, earth_radius, earth_radius) 
        layer.location = (0, 0, 0)n
        bpy.ops.object.transform_apply(scale=True)  # apply scaling

#add sunlight
if 'Sun' not in bpy.data.objects:
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10000))  # Position the Sun
    sun = bpy.context.active_object
    sun.name = 'Sun'
    print("Sunlight added.")

sun = bpy.data.objects['Sun']
sun.data.energy = 100  
sun.data.angle = 0.5  
sun.scale = (1000, 1000, 1000) 

# add world lighting
world = bpy.data.worlds['World']
world.use_nodes = True  # Enable node-based world lighting
bg_node = world.node_tree.nodes['Background']
bg_node.inputs[1].default_value = 2.5  # Boost ambient light

print("Sat & Earth layers scaled --> lighting added --> ready for rendering")
