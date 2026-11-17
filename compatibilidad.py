import numpy as np


def _perfil(borde, interior, signo):
    borde = borde.astype(np.float32)
    gradiente = signo * (borde - interior.astype(np.float32)) / 2
    return borde, gradiente


def describir_bordes(parches):
    return {
        "izquierdo": _perfil(parches[:, :, 0], parches[:, :, 2], -1),
        "derecho": _perfil(parches[:, :, -1], parches[:, :, -3], 1),
        "superior": _perfil(parches[:, 0, :], parches[:, 2, :], -1),
        "inferior": _perfil(parches[:, -1, :], parches[:, -3, :], 1),
    }


def costos_uniones(salida, entrada, d):
    B_s, G_s = salida
    B_e, G_e = entrada
    N = len(B_s)
    costos = np.empty((N, N), dtype=np.float32)

    mitad = (d + 1) / 2
    color_s = B_s + mitad * G_s
    color_e = B_e - mitad * G_e

    for i in range(N):
        costo_color = np.abs(color_s[i] - color_e).mean(axis=(1, 2))
        costo_grad = np.abs(G_s[i] - G_e).mean(axis=(1, 2))
        costos[i] = costo_color + costo_grad

    np.fill_diagonal(costos, np.inf)
    return costos


def calcular_costos(parches, d):
    bordes = describir_bordes(parches)
    D_H = costos_uniones(bordes["derecho"], bordes["izquierdo"], d)
    D_V = costos_uniones(bordes["inferior"], bordes["superior"], d)
    return D_H, D_V
