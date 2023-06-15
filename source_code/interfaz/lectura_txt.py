import sys, os

sys.path.append(os.getcwd())

import matplotlib.pyplot as plt
import math
from tkinter import filedialog as FileDialog

from tracking_utils_Entero_Canasta_1406 import (
    draw_court,
    draw_anclas,
    draw_players,
)


def lectura():
    archivotxt = FileDialog.askopenfilename(title="Abrir un fichero")
    positions_1 = []
    positions_2 = []
    positions_3 = []
    positions_4 = []
    positions_5 = []
    with open(archivotxt) as file:
        for lineas in file:
            tagid, x, y, tiempo = lineas.split(",")
            x_int = float(x)  # con el data.split() tenemos strings
            y_int = float(y)
            if tagid == "C684":
                if not math.isnan(x_int) and not math.isnan(
                    y_int
                ):  # comprueba si los valores son distintos de nan antes de añadirlos a la lista
                    positions_1.append(
                        [
                            y_int + 0.25,
                            x_int,
                        ]
                    )
            elif tagid == "9092":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_2.append([y_int + 0.25, x_int])
            elif tagid == "92AB":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_3.append([y_int + 0.25, x_int])
            elif tagid == "C70B":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_4.append([y_int + 0.25, x_int])
            elif tagid == "C9B0":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_5.append([y_int + 0.25, x_int])

    positions_1_dic = {i: v for i, v in enumerate(positions_1)}
    positions_2_dic = {i: v for i, v in enumerate(positions_2)}
    positions_3_dic = {i: v for i, v in enumerate(positions_3)}
    positions_4_dic = {i: v for i, v in enumerate(positions_4)}
    positions_5_dic = {i: v for i, v in enumerate(positions_5)}
    print(positions_2_dic)
    return (
        archivotxt,
        positions_1_dic,
        positions_2_dic,
        positions_3_dic,
        positions_4_dic,
        positions_5_dic,
    )


def grafico():
    ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
    plt.title("PISTA COMPLETA")
    draw_court(ax, grid_step=1)
    draw_anclas(ax)
    plt.show(block=False)


if __name__ == "__main__":
    archivotxt, positions1, positions2, positions3, positions4, positions5 = lectura()
    grafico()
    draw_players(
        ax=None,
        positions=positions4,
        realtime=None,
        size=0.1,
        fontsize=0,
        color="green",
        lw=1,
        numero=7,
    )
    plt.show()
