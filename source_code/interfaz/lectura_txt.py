import sys, os

sys.path.append(os.getcwd())

import matplotlib.pyplot as plt
import math
from tkinter import filedialog as FileDialog

from common.tracking_utils_entero_Canasta import BasketballCourt


def lectura():
    archivotxt = FileDialog.askopenfilename(title="Abrir un fichero")
    positions = [[], [], [], [], []]
    with open(archivotxt) as file:
        for lineas in file:
            tagid, x, y, tiempo = lineas.split(",")
            x_int = float(x)  # con el data.split() tenemos strings
            y_int = float(y)
            if tagid == "C684":
                # comprueba si los valores son distintos de nan antes de añadirlos a la lista
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions[0].append([y_int + 0.25, x_int])
            elif tagid == "9092":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions[1].append([y_int + 0.25, x_int])
            elif tagid == "92AB":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions[2].append([y_int + 0.25, x_int])
            elif tagid == "C70B":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions[3].append([y_int + 0.25, x_int])
            elif tagid == "C9B0":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions[4].append([y_int + 0.25, x_int])

    return archivotxt, positions


def grafico():
    ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
    plt.title("PISTA COMPLETA")
    BasketballCourt.draw(ax, grid_step=1)
    BasketballCourt.draw_anclas(ax)
    plt.show(block=False)


if __name__ == "__main__":
    archivotxt, positions = lectura()
    grafico()
    BasketballCourt.draw_players(
        ax=None,
        positions=positions[4],
        realtime=None,
        size=0.1,
        fontsize=0,
        color="green",
        lw=1,
        numero=7,
    )
    plt.show()
