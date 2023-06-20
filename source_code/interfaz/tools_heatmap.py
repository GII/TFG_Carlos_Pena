import sys, os

sys.path.append(os.getcwd())

import matplotlib.pyplot as plt
from tkinter import filedialog as FileDialog
from interfaz.lectura_txt import lectura


def mapacalor(positions):
    data = []
    for i in range(0, 190):
        data.append([])
        for j in range(0, 320):
            data[i].append(0)

    for position in positions:
        x = position[0]
        y = position[1] + 10
        ymin = 0
        ymax = 1
        for i in range(0, 190):
            xmin = 0
            xmax = 1
            for j in range(0, 320):
                if xmin <= x < xmax and ymin <= y < ymax:
                    data[i][j] = data[i][j] + 1
                xmin = xmin + 0.1
                xmax = xmax + 0.1
            ymin = ymin + 0.1
            ymax = ymax + 0.1
    return data


if __name__ == "__main__":
    archivotxt, positions = lectura()
    data = mapacalor(positions[0])
    fig, ax = plt.subplots()
    ax.imshow(
        data,
        cmap="nipy_spectral",
        norm="asinh",
        aspect="auto",
        alpha=1,
        interpolation="nearest",
        origin="lower",
        extent=(0, 32, 0, 19),
    )
    plt.show()
