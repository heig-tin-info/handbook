import matplotlib.pyplot as plt
import numpy as np


def sin_rmsd(z):
    a = 1.5704
    b = 0.6427
    c = 0.0724
    return a * z - b * z**3 + c * z**5


def sin_naive(z):
    a = np.pi / 2
    b = np.pi - 5 / 2
    c = np.pi / 2 - 3 / 2
    return a * z - b * z**3 + c * z**5


def sin_coranac(z):
    a = 4 * (3 / np.pi - 9 / 16)
    b = 2 * a - 5 / 2
    c = a - 3 / 2
    return a * z - b * z**3 + c * z**5


def x_to_z(x):
    return x / (np.pi / 2)


x_vals = np.linspace(0, np.pi / 2, 100)
z_vals = x_to_z(x_vals)
sin_vals = np.sin(x_vals)  # Sinus exact

fig, ax = plt.subplots(figsize=(8, 4))  # 4/2 aspect ratio (in inches)

# Plot the error differences
ax.plot(z_vals, (sin_naive(z_vals) - sin_vals), label="Naive", linestyle="-")
ax.plot(z_vals, (sin_rmsd(z_vals) - sin_vals), label="RMSD", linestyle="-.")
ax.plot(z_vals, (sin_coranac(z_vals) - sin_vals), label="Coranac", linestyle=":")


# Set labels
ax.set_xlabel("z (x / (pi/2))")
ax.set_ylabel("Erreur en ‰")

# Customize ticks
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: "{:.1f}".format(val)))
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda val, pos: "{:.1f}".format(val * 1000))
)

# Add grid, legend and title
ax.grid(True, which="both", axis="both", linestyle="--", linewidth=0.5)
ax.legend()

# Display the plot
plt.tight_layout()
plt.show()
