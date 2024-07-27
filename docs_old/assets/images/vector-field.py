import numpy as np
import matplotlib.pyplot as plt

# Create a smoother and convex surface with finer grid but fewer vectors
x = np.linspace(-1, 1, 30)
y = np.linspace(-1, 1, 30)
x, y = np.meshgrid(x, y)
z = -(x**2 + y**2)

# Calculate the normal vectors
dz_dx, dz_dy = np.gradient(z)
normal_x = -dz_dx
normal_y = -dz_dy
normal_z = np.ones_like(z)

# Normalize the normal vectors
norm = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
normal_x /= norm
normal_y /= norm
normal_z /= norm

# Select fewer points for vectors
step = 4
x_vec = x[::step, ::step]
y_vec = y[::step, ::step]
z_vec = z[::step, ::step]
normal_x_vec = normal_x[::step, ::step]
normal_y_vec = normal_y[::step, ::step]
normal_z_vec = normal_z[::step, ::step]

# Plot the surface and normal vectors
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, color='yellow', alpha=0.7)

# Scale normal vectors for better visualization
scale = 0.5
ax.quiver(x_vec, y_vec, z_vec, normal_x_vec * scale, normal_y_vec * scale, normal_z_vec * scale, color='blue')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.savefig('vector-field.svg')
