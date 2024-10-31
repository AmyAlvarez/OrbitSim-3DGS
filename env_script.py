import bpy
import numpy as np

#parameters for the corkscrew orbit path
radius = 500  #changed scaling for visualization (change later to scale correctly)
inclination = 45 * np.pi / 180  #inclination in radians (45 degrees)
h = 200  #altitude --> affects the calculation of orbital period
T = 2 * np.pi * np.sqrt((6378.137 + h)**3 / 398600.44)  #orbital period
om = 2 * np.pi / T  #angular velocity
t = np.linspace(0, 2 * T, 1000)  #time samples to create a smooth path

#calculate the corkscrew path trajectory points
x_t = radius * np.cos(om * t)  # circular motion in the x-direction
y_t = radius * np.sin(inclination) * np.sin(om * t)  #inclined circular motion in y
z_t = np.linspace(-radius, radius, len(t))  #vertical spiral effect for corkscrew

#create the corkscrew path in Blender
curve_data = bpy.data.curves.new(name='CorkscrewOrbit', type='CURVE')
curve_data.dimensions = '3D'
polyline = curve_data.splines.new('POLY')

#set the number of points for the curve
polyline.points.add(len(x_t) - 1)

#add each calculated point to the polyline
for i, (x, y, z) in enumerate(zip(x_t, y_t, z_t)):
    polyline.points[i].co = (x, y, z, 1)  

#create a new object with the curve data
orbit_path = bpy.data.objects.new('CorkscrewOrbitObject', curve_data)
bpy.context.collection.objects.link(orbit_path)

print("Corkscrew orbit path created.")

#get references to the corkscrew path, Surface (Earth), and satellite objects
orbit_path = bpy.data.objects['CorkscrewOrbitObject.001']  #corkscrew orbit path
surface = bpy.data.objects['Surface']  #earth model, with Atmo and Clouds parented
satellite = bpy.data.objects['Satellite']  #satellite model

#set the animation duration for the corkscrew orbit path
#esure the duration matches the orbital period
T = orbit_path.data.path_duration  

#attach Earth (Surface) to the path
#add a Follow Path constraint to Surface
surface_constraint = surface.constraints.new(type='FOLLOW_PATH')
surface_constraint.target = orbit_path
surface_constraint.use_curve_follow = True

#set keyframes for Surface to move along the path
surface_constraint.offset_factor = 0  #start at the beginning of the path
surface.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=1)
surface_constraint.offset_factor = 1  #move to the end of the path
surface.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=int(T))

print("Earth is following the corkscrew path.")

#attach Satellite to the path
#add a Follow Path constraint to the Satellite
satellite_constraint = satellite.constraints.new(type='FOLLOW_PATH')
satellite_constraint.target = orbit_path
satellite_constraint.use_curve_follow = True

#set keyframes for Satellite to move along the path
satellite_constraint.offset_factor = 0  #start at the beginning of the path
satellite.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=1)
satellite_constraint.offset_factor = 1  #move to the end of the path
satellite.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=int(T))

print("Satellite is following the corkscrew path.")

