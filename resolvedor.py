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
        self.tamaño_celda = None
        self.plano_real = np.full((r, c), None, dtype=object)
        self.piezas_usadas = {self.pos_og_pieza_ancl}
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
        row_real, col_real = self.pos_new_pieza_ancl
        self.plano_real[row_real, col_real] = self.pos_og_pieza_ancl

    def resolver_imagen(self):
        if self.tamaño_celda is None:
            self.obtener_ubi_celdas()

        s_y, s_x = self.tamaño_celda
        y, x = self.ubicacion_init_celdas[self.pos_og_pieza_ancl]
        borde_up    = self.img[y, x : x + s_x]
        borde_down  = self.img[y + s_y - 1, x : x + s_x]
        borde_left  = self.img[y : y + s_y, x]
        borde_right = self.img[y : y + s_y, x + s_x - 1]

        row_real, col_real = self.pos_new_pieza_ancl

        if row_real + 1 < self.r:
            s = self.comparar_borde(borde_down, 0)
            if s is not None:
                self.plano_real[row_real + 1, col_real] = s
                self.piezas_usadas.add(s)

        if col_real + 1 < self.c:
            d = self.comparar_borde(borde_right, 1)
            if d is not None:
                self.plano_real[row_real, col_real + 1] = d
                self.piezas_usadas.add(d)

        if row_real - 1 >= 0:
            w = self.comparar_borde(borde_up, 2)
            if w is not None:
                self.plano_real[row_real - 1, col_real] = w
                self.piezas_usadas.add(w)

        if col_real - 1 >= 0:
            a = self.comparar_borde(borde_left, 3)
            if a is not None:
                self.plano_real[row_real, col_real - 1] = a
                self.piezas_usadas.add(a)

    def comparar_borde(self, borde, direccion):
        #pos posible
        #abajo = 0, derecha = 1, arriba = 2, izquierda = 3
        #dara None si no hay y la pos si hay 
        s_y, s_x = self.tamaño_celda
        best = None
        best_diff = float("inf")
        borde_f = borde.astype(np.float32)

        for n in range(self.r):
            for m in range(self.c):
                if (n, m) in self.piezas_usadas:
                    continue

                y, x = self.ubicacion_init_celdas[n, m]

                if direccion == 0:
                    borde_comp = self.img[y, x : x + s_x]
                elif direccion == 1:
                    borde_comp = self.img[y : y + s_y, x]
                elif direccion == 2:
                    borde_comp = self.img[y + s_y - 1, x : x + s_x]
                elif direccion == 3:
                    borde_comp = self.img[y : y + s_y, x + s_x - 1]

                diff = np.mean(np.abs(borde_comp.astype(np.float32) - borde_f))
                if diff < self.VALOR_BORDE and diff < best_diff:
                    best = (n, m)
                    best_diff = diff
        return best