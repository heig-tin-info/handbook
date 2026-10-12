import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve


def sin_pi_over_2(x):
    return np.sin(np.pi * x / 2)


def z_power_n(n, x):
    return x**n


integrals_matrix = np.zeros((3, 3))
for i, n1 in enumerate([5, 3, 1]):
    for j, n2 in enumerate([5, 3, 1]):
        integrals_matrix[i, j] = quad(lambda x: z_power_n(n1 + n2, x), 0, 1)[0]

integrals_rhs = np.zeros(3)
for i, n in enumerate([5, 3, 1]):
    integrals_rhs[i] = quad(lambda x: sin_pi_over_2(x) * z_power_n(n, x), 0, 1)[0]

a, b, c = solve(integrals_matrix, integrals_rhs)
print(a, b, c)
