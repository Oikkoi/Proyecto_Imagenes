
import numpy as np
def estimar_d(mosaico, R, C):
    

    H, W, _ = mosaico.shape
    
    s_h, s_w = H // R, W // C

    # Ejes = fila de celda, fila local, columna de celda, columna local, RGB.
    celdas = mosaico.reshape(R, s_h, C, s_w, 3)

    for d in (5, 3, 1, 0):
        if not (64 <= s_h - d <= 512 and 64 <= s_w - d <= 512):
            continue

        if d == 0:
            return 0  # No habrian mas margenes que revisar

        q = d // 2
        posterior = d - q

        superior = celdas[:, :q, :, :, :]
        inferior = celdas[:, s_h - posterior:, :, :, :]
        izquierdo = celdas[:, :, :, :q, :]
        derecho = celdas[:, :, :, s_w - posterior:, :]

        if not (
            np.any(superior)
            or np.any(inferior)
            or np.any(izquierdo)
            or np.any(derecho)
        ):
            return d
