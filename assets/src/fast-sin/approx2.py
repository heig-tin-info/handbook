import matplotlib.pyplot as plt
import numpy as np


def poly_sin_approx2(z):
    a = 1.5704
    b = 0.6427
    c = 0.0724
    return a * z - b * z**3 + c * z**5


def poly_sin_approx3(z):
    c = 2 / np.pi
    b = 1 / np.pi
    a = 2 / np.pi**3
    return a * z - b * z**3 + c * z**5


def poly_sin_approx1(z):
    a = np.pi / 2.0
    b = np.pi - 5.0 / 2.0
    c = np.pi / 2 - 3.0 / 2.0
    return a * z - b * z**3 + c * z**5


def poly_sin_approx(z):
    a5 = 4 * (3 / np.pi - 9 / 16)
    b5 = 2 * a5 - 5 / 2
    c5 = a5 - 3 / 2
    return a5 * z - b5 * z**3 + c5 * z**5


# Transformation x -> z, où z = x / (pi/2)
def x_to_z(x):
    return x / (np.pi / 2)


# Fonction pour les approximations en Q1.15
def to_q15(value):
    return int(value * 32768)


def from_q15(value):
    return value / 32768


# Padé-Chebyshev Q1.15
def sin16_pade_q15(x_q15):
    x = from_q15(x_q15)
    num = 4 * x * (180 - x)  # Numérateur
    denom = 40500 - x * (180 - x)  # Dénominateur
    result = num / denom
    return to_q15(result)


# Remez approximation Q1.15
def sin16_remez_q15(x_q15):
    x = from_q15(x_q15)
    x2 = x * x
    x3 = x2 * x
    x5 = x3 * x2
    result = x - (x3 / 6) + (x5 / 120)
    return to_q15(result)


# CORDIC approximation Q1.15
cordic_angles_q15 = [
    to_q15(np.deg2rad(angle))
    for angle in [45, 26.565, 14.036, 7.125, 3.576, 1.789, 0.895, 0.448]
]


def cordic_q15(theta_q15):
    K_q15 = to_q15(0.607252935)  # Facteur de normalisation
    x_q15 = K_q15
    y_q15 = 0
    z_q15 = theta_q15

    for i in range(8):
        x_new, y_new = 0, 0
        if z_q15 < 0:
            x_new = x_q15 + (y_q15 >> i)
            y_new = y_q15 - (x_q15 >> i)
            z_q15 += cordic_angles_q15[i]
        else:
            x_new = x_q15 - (y_q15 >> i)
            y_new = y_q15 + (x_q15 >> i)
            z_q15 -= cordic_angles_q15[i]
        x_q15, y_q15 = x_new, y_new

    return y_q15  # Retourne le sinus en Q1.15


# Transformation des valeurs en Q1.15 pour tester les fonctions
theta_degrees = 45
theta_q15 = to_q15(np.deg2rad(theta_degrees))

# Résultats des approximations
sin_pade_q15 = sin16_pade_q15(theta_q15)
sin_remez_q15 = sin16_remez_q15(theta_q15)
sin_cordic_q15 = cordic_q15(theta_q15)

sin_pade_q15, sin_remez_q15, sin_cordic_q15


# Génération des valeurs pour x (angles entre 0 et pi/2) et z (valeurs normalisées entre 0 et 1)
x_vals = np.linspace(0, np.pi / 2, 100)
z_vals = x_to_z(x_vals)
sin_vals = np.sin(x_vals)  # Sinus exact
approx_vals = poly_sin_approx(z_vals)  # Approximation polynomiale
approx_vals1 = poly_sin_approx1(z_vals)  # Approximation polynomiale
approx_vals2 = poly_sin_approx2(z_vals)  # Approximation polynomiale
approx_vals3 = poly_sin_approx3(z_vals)  # Approximation polynomiale

# Conversion des valeurs en Q1.15 pour les trois méthodes
# z_vals_q15 = [to_q15(z) for z in z_vals]
# sin_pade_q15_vals = [from_q15(sin16_pade_q15(z_q15)) for z_q15 in z_vals_q15]
# sin_remez_q15_vals = [from_q15(sin16_remez_q15(z_q15)) for z_q15 in z_vals_q15]
# sin_cordic_q15_vals = [from_q15(cordic_q15(z_q15)) for z_q15 in z_vals_q15]

# Tracé des résultats pour les quatre méthodes
# plt.plot(z_vals, sin_vals, label="Sinus exact", linestyle="--")
plt.plot(z_vals, approx_vals - sin_vals, label="Minimise erreur", linestyle="-")
plt.plot(z_vals, approx_vals1 - sin_vals, label="Naïf", linestyle=":")
plt.plot(z_vals, approx_vals2 - sin_vals, label="Moindre carrés", linestyle="-.")
plt.plot(z_vals, approx_vals3 - sin_vals, label="Moindre carrés2", linestyle=":")
# plt.plot(z_vals, sin_pade_q15_vals, label="Padé-Chebyshev Q1.15", linestyle=":")
# plt.plot(z_vals, sin_remez_q15_vals, label="Remez Q1.15", linestyle="-.")
# plt.plot(z_vals, sin_cordic_q15_vals, label="CORDIC Q1.15", linestyle=":")

plt.xlabel("z (x / (pi/2))")
plt.ylabel("Valeur du sinus")
plt.title("Comparaison entre sinus exact et approximations")
plt.legend()
plt.grid(True)
plt.show()
