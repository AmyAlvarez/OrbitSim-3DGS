import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# parameters for the orbit
radius = 50  # radius of circular motion (in meters)
vertical_amplitude = 20  # vertical oscillation (m)
frequency = 0.05  # frequency of oscillation (affects how many lobes appear)
num_cycles = 2  # number of full oscillation cycles

# time vector
t = np.linspace(0, 2 * np.pi * num_cycles, 1000)

# modified corkscrew trajectory
x_t = radius * np.cos(t)  # circular motion along the X-axis
y_t = radius * np.sin(t)  # circular motion along the Y-axis
z_t = vertical_amplitude * np.sin(frequency * t)  # oscillating motion along the Z-axis

# plotting 2D views: x vs z
plt.figure(figsize=(12, 6))

# x vs z view
plt.subplot(1, 2, 1)
plt.plot(x_t, z_t, label='Orbit')
plt.scatter([0], [0], color='orange', label='Target Spacecraft')
plt.xlabel('X Position')
plt.ylabel('Z Position')
plt.title('Modified Corkscrew Orbit (X-Z View)')
plt.legend()

# 3D view
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot3D(x_t, y_t, z_t, label='Corkscrew Orbit')
ax.scatter([0], [0], [0], color='orange', label='Target Spacecraft')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')
ax.set_title('3D Corkscrew Orbit')
ax.legend()

plt.show()
