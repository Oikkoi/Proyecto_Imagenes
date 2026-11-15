import numpy as np
from skimage import io
import os
import matplotlib.pyplot as plt
import cv2
import scipy


def verificar_imagen(path_imagen: str) -> np.array:
    # Revisar que exista la imagen
    ruta_completa = os.path.join(os.path.dirname(__file__), path_imagen)
    if not os.path.isfile(ruta_completa):
        raise ValueError("No existe el archivo")
    imagen = io.imread(ruta_completa)
    # Revisar que sea RGB
    if (imagen.ndim != 3) or (imagen.shape[2] != 3):
        raise ValueError("La imagen no es RGB")
    # Revisar que sea uint8
    if imagen.dtype != np.uint8:
        raise ValueError("La imagen debe ser de 8 bits (uint8).")
    return imagen


def verificar_medidas(imagen: np.array, R: int, C: int, d: int):
    # definimos los valores válidos
    valores_R_C = (4, 5, 6, 7, 8, 9)
    valores_d = (0, 1, 3, 5)
    # revisamos que los parámetros de entrada cumplan
    if R not in valores_R_C:
        raise ValueError(f"R no es un entero de {valores_R_C}")
    if C not in valores_R_C:
        raise ValueError(f"C no es un entero de {valores_R_C}")
    if d not in valores_d:
        raise ValueError(f"d no pertenece a {valores_d}")
    # definir forma del parche
    alto, ancho, _ = imagen.shape
    s_ancho = ancho // C
    s_alto = alto // R
    parche_ancho = s_ancho - d
    parche_alto = s_alto - d
    # revisar valores límites del parche
    if not (64 <= parche_alto <= 512):
        raise ValueError(
            f"El valor del alto del parche excede los límites (entre 64 y 512). s_alto = {s_alto}")
    if not (64 <= parche_ancho <= 512):
        raise ValueError(
            f"El valor del ancho del parche excede los límites (entre 64 y 512). s_ancho = {s_ancho}")
    # revisar que (tamaño parche) *(numero de parches) = (dimensiones originales)
    if (ancho < (s_ancho * C)) or (alto < (s_alto * R)):
        raise ValueError(
            "Fallos en la construcción. El resultado es más grande que la entrada")
    return ((s_alto, s_ancho), (parche_alto, parche_ancho), (R, C, d))


def generar_mosaico(imagen: np.array, tupla_s_p: tuple, seed: int):
    alto, ancho, _ = imagen.shape
    tupla_s, tupla_p, parametros = tupla_s_p
    s_alto, s_ancho = tupla_s
    R, C, d = parametros
    H = R * s_alto
    W = C * s_ancho

    """
    Por construcción, puede haber diferencia entre el alto real y H; y el ancho y W. Por eso, hay que hacer el recorte de
    los píxeles no considerados entre ambos bordes:
    """

    # slicing imagen
    fila_inicial = (alto - H) // 2
    fila_fin = fila_inicial + H
    columna_inicial = (ancho - W) // 2
    columna_fin = columna_inicial + W
    sub_imagen = imagen[fila_inicial:fila_fin, columna_inicial:columna_fin]

    # lienzo
    zeros = np.zeros((H, W, 3), dtype=np.uint8)
    parche_alto, parche_ancho = tupla_p
    margen = d // 2
    rng = np.random.default_rng(seed)
    permutacion = rng.permutation(R * C)

    matriz_identificadores = np.zeros((R, C), dtype=int)

    for k, indice_real in enumerate(permutacion):
        # Coordenadas de celda en el mosaico desordenado (r_s, c_s)
        fila_mosaico = k // C
        columna_mosaico = k % C

        # Coordenadas de celda en la imagen recortada (r_t, c_t)
        fila_real = indice_real // C
        columna_real = indice_real % C

        # Límites del recorte en sub_imagen
        fila_real_inicial = fila_real * s_alto + margen
        fila_real_fin = fila_real_inicial + parche_alto
        columna_real_inicial = columna_real * s_ancho + margen
        columna_real_fin = columna_real_inicial + parche_ancho

        # Límites donde se pega el parche en zeros
        fila_mosaico_inicial = fila_mosaico * s_alto + margen
        fila_mosaico_fin = fila_mosaico_inicial + parche_alto
        columna_mosaico_inicial = columna_mosaico * s_ancho + margen
        columna_mosaico_fin = columna_mosaico_inicial + parche_ancho

        # Copiar parche útil al lienzo
        zeros[
            fila_mosaico_inicial:fila_mosaico_fin,
            columna_mosaico_inicial:columna_mosaico_fin,
        ] = sub_imagen[
            fila_real_inicial:fila_real_fin,
            columna_real_inicial:columna_real_fin,
        ]

        # Guardar identificador (convención desde 1: k + 1)
        matriz_identificadores[fila_real, columna_real] = k + 1

    # Anclaje aleatorio en convención desde 1: ((r_s, c_s), (r_t, c_t))
    k_anclaje = int(rng.integers(0, R * C))
    indice_real_anclaje = int(permutacion[k_anclaje])

    fila_anclaje_s = (k_anclaje // C) + 1
    columna_anclaje_s = (k_anclaje % C) + 1
    fila_anclaje_t = (indice_real_anclaje // C) + 1
    columna_anclaje_t = (indice_real_anclaje % C) + 1

    anclaje = ((fila_anclaje_s, columna_anclaje_s),
               (fila_anclaje_t, columna_anclaje_t))

    return (zeros, matriz_identificadores, anclaje)


if __name__ == "__main__":
    carpeta_actual = os.path.dirname(__file__)
    path_imagen = "test.jpg"
    imagen = verificar_imagen(path_imagen)
    tupla_s_p = verificar_medidas(imagen, 9, 9, 3)
    mosaico, matriz_identificadores, anclaje = generar_mosaico(
        imagen, tupla_s_p, seed=42)

    io.imsave(os.path.join(carpeta_actual, "mosaico.png"), mosaico)
    np.savez(
        os.path.join(carpeta_actual, "referencia.npz"),
        P_GT=matriz_identificadores,
        anclaje=np.array(anclaje),
    )
