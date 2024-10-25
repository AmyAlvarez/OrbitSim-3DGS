import bpy
import numpy as np

# corkscrew parameters
radius = 10
inclination = 45 * np.pi / 180 
xo, yo, zo = radius, 0, 0  
h = 200 
T = 2 * np.pi * np.sqrt((6378.137 + h)**3 / 398600.44)  #orbital period
om = 2 * np.pi / T  #angular velocity
t = np.linspace(0, 2 * T, 1000)  #time samples

#velocity components
xod = 0
yod = radius * np.sin(inclination) * om
zod = -radius * np.sin(inclination) * om

#trajectory equations
x_t = -2 * zod * np.cos(om * t) / om + (xo + 2 * zod / om)
y_t = yod * np.sin(om * t) / om
z_t = zod * np.sin(om * t) / om

#visualize via belnder
#create path and points in blender
curve_data = bpy.data.curves.new(name='CorkscrewOrbit', type='CURVE')
curve_data.dimensions = '3D'
polyline = curve_data.splines.new('POLY')

#set the number of points
polyline.points.add(len(x_t) - 1)

# Add the calculated points to the polyline
for i, (x, y, z) in enumerate(zip(x_t, y_t, z_t)):
    polyline.points[i].co = (x, y, z, 1)  # 1 for homogeneous coordinate

# Create a new object with the curve data
orbit_object = bpy.data.objects.new('CorkscrewOrbitObject', curve_data)
bpy.context.collection.objects.link(orbit_object)
