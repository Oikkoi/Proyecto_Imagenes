import cv2
import numpy as np

class Resolvedor:
    def __init__(self, img, r, c, anclaje):
        self.img = img
        self.ubicacion_init_celdas = np.zeros((r, c, 2), dtype=int)
        self.final_img = None
        self.r = r
        self.c = c
        self.anclaje = anclaje
        self.d = None

    def estimar_d(self):
        pass

    def obtener_ubi_celdas(self):
        if self.d is None:
            self.estimar_d()
        height, width = self.img.shape[:2]
        height_celda = height // self.r
        width_celda = width // self.c
        q = self.d // 2
        for n in range(self.r):
            row = height_celda * n + q
            for m in range(self.c):
                col = width_celda * m + q
                self.ubicacion_init_celdas[n, m] = (row, col)
 



    def comparar_borde(borde, pos):
        #pos posible
        #arriba = 0, derecha = 1, abajo = 2, izquierda = 3
        pass






if __name__ == "__main__":
    img = cv2.imread("mosaico.png")
    resolvedor = Resolvedor(img)