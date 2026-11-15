import numpy as np
from skimage import io
import os
import matplotlib.pyplot as plt
import cv2
import scipy


def verificar_imagen(path_imagen: str) -> np.array:
    if not os.isdir(os.path.join(__file__, path_imagen)):
        raise ValueError("No existe el archivo")
    return


if __name__ == "__main__":
    print("si compila")
    verificar_imagen("test_image.png")
