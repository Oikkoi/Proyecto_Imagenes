from pathlib import Path

import numpy as np


def adyacencias(P):
    """Devuelve los pares ordenados izquierda-derecha y arriba-abajo."""
    horizontales = set(zip(P[:, :-1].ravel(), P[:, 1:].ravel()))
    verticales = set(zip(P[:-1, :].ravel(), P[1:, :].ravel()))
    return horizontales, verticales

