# Import numpy for calculations
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg")
# Définition des coefficients donnés pour l'approximation polynomiale
a5 = 4 * (3 / np.pi - 9 / 16)
b5 = 2 * a5 - 5 / 2
c5 = a5 - 3 / 2


# Approximation polynomiale sin_5(x) = a_5z - b_5z^3 + c_5z^5
def poly_sin_approx(z):
    return a5 * z - b5 * z**3 + c5 * z**5


# Transformation x -> z, où z = x / (pi/2)
def x_to_z(x):
    return x / (np.pi / 2)


# Génération des valeurs pour x (angles entre 0 et pi/2) et z (valeurs normalisées entre 0 et 1)
x_vals = np.linspace(0, np.pi / 2, 100)
z_vals = x_to_z(x_vals)
sin_vals = np.sin(x_vals)
approx_vals = poly_sin_approx(z_vals)

# Tracé des résultats
plt.plot(z_vals, sin_vals, label="Sinus exact", linestyle="--")
plt.plot(z_vals, approx_vals, label="Approximation polynomiale", linestyle="-")
plt.xlabel("z (x / (pi/2))")
plt.ylabel("Valeur du sinus")
plt.title("Comparaison entre sinus exact et approximation polynomiale")
plt.legend()
plt.grid(True)
plt.show()

# Affichage des coefficients
a5, b5, c5
