from pathlib import Path
import numpy as np


def adyacencias(P):
    """Devuelve los pares ordenados izquierda-derecha y arriba-abajo."""
    horizontales = set(zip(P[:, :-1].ravel(), P[:, 1:].ravel()))
    verticales = set(zip(P[:-1, :].ravel(), P[1:, :].ravel()))
    return horizontales, verticales


def evaluar(P_hat, P_GT):
    P_hat = np.asarray(P_hat)
    P_GT = np.asarray(P_GT)
    if P_GT.ndim != 2 or P_GT.size < 2 or P_hat.shape != P_GT.shape:
        raise ValueError("P_hat y P_GT deben ser matrices del mismo tamaño con al menos dos parches.")

    R, C = P_GT.shape
    ids = np.arange(1, R * C + 1)
    for nombre, P in (("P_hat", P_hat), ("P_GT", P_GT)):
        if not np.issubdtype(P.dtype, np.integer) or not np.array_equal(np.sort(P.ravel()), ids):
            raise ValueError(f"{nombre} debe contener una vez cada identificador de 1 a {R * C}.")

    A_pos = np.count_nonzero(P_hat == P_GT) / (R * C)
    H_hat, V_hat = adyacencias(P_hat)
    H_GT, V_GT = adyacencias(P_GT)
    correctas = len(H_hat & H_GT) + len(V_hat & V_GT)
    A_adj = correctas / (R * (C - 1) + (R - 1) * C)
    return A_pos, A_adj



# TESTEO 
P_GT = np.arange(1, 17).reshape(4, 4)

# Reconstrucción correcta
assert evaluar(P_GT.copy(), P_GT) == (1.0, 1.0)

# Desplazamiento circular de una columna
P_hat = np.roll(P_GT, 1, axis=1)
A_pos, A_adj = evaluar(P_hat, P_GT)
assert A_pos == 0.0
assert np.isclose(A_adj, 20 / 24)

# La transposición convierte rota bien los vecinos
assert evaluar(P_GT.T, P_GT) == (0.25, 0.0)

print("Las tres pruebas pasaron yippiee .")