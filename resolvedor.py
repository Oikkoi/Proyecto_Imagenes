from skimage import io
import numpy as np
from estimador_d import estimar_d


class Resolvedor:
    def __init__(self, img, r, c, anclaje):
        self.img = img
        self.ubicacion_init_celdas = np.zeros((r, c, 2), dtype=int)
        self.final_img = None
        self.r = r
        self.c = c
        self.pos_og_pieza_ancl = (anclaje[0][0] - 1, anclaje[0][1] - 1)
        self.pos_new_pieza_ancl = (anclaje[1][0] - 1, anclaje[1][1] - 1)
        self.d = None
        self.plano_real = np.full((r, c), None, dtype=object)
        self.VALOR_BORDE = 30
    
    def estimar_d(self):
        self.d = estimar_d(self.img, self.r, self.c)

    def obtener_ubi_celdas(self):
        if self.d is None:
            self.estimar_d()
        height, width = self.img.shape[:2]
        height_celda = height // self.r
        width_celda = width // self.c
        self.tamaño_celda = (height_celda - self.d, width_celda - self.d)
        q = self.d // 2
        for n in range(self.r):
            row = height_celda * n + q
            for m in range(self.c):
                col = width_celda * m + q
                self.ubicacion_init_celdas[n, m] = (row, col)
                if (n, m) == self.pos_og_pieza_ancl:
                    self.pos_og_real = (row, col)
                    self.plano_real[n, m] = (row, col)
                    self.row_og = n
                    self.col_og = m


    def resolver_imagen(self):
        s_y, s_x = self.tamaño_celda
        y, x = self.pos_og_real
        borde_up = self.img[y, x : x + s_x]
        borde_down = self.img[y + s_y - 1, x : x + s_x]
        borde_left = self.img[y : y + s_y, x]
        borde_right = self.img[y : y + s_y, x + s_x - 1]
        s = self.comparar_borde(borde_down, 0)
        d = self.comparar_borde(borde_right, 1)
        w = self.comparar_borde(borde_up, 2)
        a = self.comparar_borde(borde_left, 3)

        if s:
            if s not in self.plano_real:
                self.plano_real[self.row_og - 1, self.col_og] = s

        if d:
            if d not in self.plano_real:
                self.plano_real[self.row_og, self.col_og + 1] = s

        if w:
            if w not in self.plano_real:
                self.plano_real[self.row_og - 1, self.col_og] = s

        if a:
            if a not in self.plano_real:
                self.plano_real[self.row_og, self.col_og - 1] = a


        



    def comparar_borde(self, borde, pos):
        #pos posible
        #abajo = 0, derecha = 1, arriba = 2, izquierda = 3
        #dara None si no hay y la pos si hay 
        s_y, s_x = self.tamaño_celda
        best = None
        best_diff = 255 * 3
        for pos in self.ubicacion_init_celdas:
            x, y = pos
            if pos == 0:
                borde_comp = self.img[y, x : x + s_x]
            if pos == 2:
                borde_comp = self.img[y + s_y - 1, x : x + s_x]
            if pos == 1:
                borde_comp = self.img[y : y + s_y, x]
            if pos == 3:
                borde_comp = self.img[y : y + s_y, x + s_x - 1]

            diff = borde_comp - borde
            if sum(diff) < self.VALOR_BORDE:
                if sum(diff) < best_diff:
                    best = pos
                    best_diff = sum(diff)
        return best






if __name__ == "__main__":
    pass