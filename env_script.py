import bpy
import numpy as np
from mathutils import Matrix

# parameters for the corkscrew orbit path
radius = 500
inclination = 45 * np.pi / 180  # 45 degrees in radians
h = 200  # Altitude
T = 2 * np.pi * np.sqrt((6378.137 + h)**3 / 398600.44)  # orbital period
om = 2 * np.pi / T
t = np.linspace(0, 2 * T, 1000)  # time samples for smooth path

# generate corkscrew orbit path points
x_t = radius * np.cos(om * t)
y_t = radius * np.sin(inclination) * np.sin(om * t)
z_t = np.linspace(-radius, radius, len(t))

# corkscrew orbit path creation
curve_data = bpy.data.curves.new(name='CorkscrewOrbit', type='CURVE')
curve_data.dimensions = '3D'
polyline = curve_data.splines.new('POLY')
polyline.points.add(len(x_t) - 1)

for i, (x, y, z) in enumerate(zip(x_t, y_t, z_t)):
    polyline.points[i].co = (x, y, z, 1)  # Add points to the curve

orbit_path = bpy.data.objects.new('CorkscrewOrbitObject', curve_data)
bpy.context.collection.objects.link(orbit_path)

print("corkscrew orbit path created successfully")

# get earth, satellite, and camera objects
earth = bpy.data.objects.get('Surface')
satellite = bpy.data.objects.get('Satellite')
camera = bpy.data.objects.get('Camera2')  # get Camera object

# error handling
if earth is None:
    raise KeyError("earth (Surface) object not found in the scene ")
if satellite is None:
    raise KeyError("satellite object not found in the scene ")
if camera is None:
    raise KeyError("camera object not found in the scene ")

# parent the camera to the satellite
camera.parent = satellite
camera.matrix_parent_inverse = satellite.matrix_world.inverted()

# animate the satellite along the corkscrew path
satellite_constraint = satellite.constraints.new(type='FOLLOW_PATH')
satellite_constraint.target = orbit_path
satellite_constraint.use_curve_follow = True
satellite_constraint.forward_axis = 'FORWARD_X'
satellite_constraint.up_axis = 'UP_Z'

# set keyframes for animation
satellite_constraint.offset_factor = 0
satellite.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=1)
satellite_constraint.offset_factor = 1
satellite.keyframe_insert(data_path='constraints["Follow Path"].offset_factor', frame=int(T))

print("Satellite animation set up successfully.")

# satellite LVLH orientation calculation
def calculate_lvlh_orientation(position, earth_position):
    # convert positions to numpy arrays
    position = np.array(position)
    earth_position = np.array(earth_position)
    
    # direction toward Earth (z-axis)
    direction_to_earth = earth_position - position
    z_axis = direction_to_earth / np.linalg.norm(direction_to_earth)
    
    # forward direction for x-axis
    forward_direction = np.cross(z_axis, [0, 0, 1])  # use an arbitrary up vector
    x_axis = forward_direction / np.linalg.norm(forward_direction)
    
    # perpendicular direction for y-axis
    y_axis = np.cross(z_axis, x_axis)
    
    # return the rotation matrix as a Blender-compatible Matrix object
    return Matrix([x_axis, y_axis, z_axis]).transposed()

# apply the LVLH orientation to the satellite
satellite.location = (x_t[0], y_t[0], z_t[0])

# get the LVLH rotation matrix
lvlh_orientation_matrix = calculate_lvlh_orientation(satellite.location, earth.location)

# convert the matrix to Euler angles and assign to the satellite
satellite.rotation_euler = lvlh_orientation_matrix.to_euler()

print("satellite LVLH orientation applied successfully")

# ensure Earth is stationary
# no constraints are applied to Earth --> only satellite moves around it

# set path duration to match orbital period
orbit_path.data.path_duration = int(T)
print("animation duration set for the corkscrew path")
