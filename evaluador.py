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

    R, C = P_GT.shape
    ids = np.arange(1, R * C + 1)

    A_pos = np.count_nonzero(P_hat == P_GT) / (R * C)
    H_hat, V_hat = adyacencias(P_hat)
    H_GT, V_GT = adyacencias(P_GT)
    correctas = len(H_hat & H_GT) + len(V_hat & V_GT)
    A_adj = correctas / (R * (C - 1) + (R - 1) * C)
    return A_pos, A_adj
