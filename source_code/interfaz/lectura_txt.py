import sys, os

sys.path.append(os.getcwd())

import numpy as np
import matplotlib.pyplot as plt
import math
from tkinter import filedialog as FileDialog

from common.tracking_utils_entero_Canasta import (
    draw_court,
    draw_anclas,
    draw_players,
)

# POSIBILIDAD DE SACAR 5 GRÁFICAS, 1 POR JUGADOR ???


def lectura():
    archivotxt = FileDialog.askopenfilename(title="Abrir un fichero")
    positions_1 = []
    positions_2 = []
    positions_3 = []
    positions_4 = []
    positions_5 = []
    with open(archivotxt) as file:
        for lineas in file:
            tagid, x, y = lineas.split(",")
            x_int = float(x)  # con el data.split() tenemos strings
            y_int = float(y)
            if tagid == "9092":
                if not math.isnan(x_int) and not math.isnan(
                    y_int
                ):  # comprueba si los valores son distintos de nan antes de añadirlos a la lista
                    positions_1.append(
                        [
                            y_int + 0.25,
                            x_int,
                        ]  # Ajustes a los ejes para TomaDatos_0505 y + 4.3 , -x + 0.8
                    )
            elif tagid == "C684":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_2.append([y_int + 0.25, x_int])
            elif tagid == "XXXX":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_3.append([y_int + 0.25, x_int])
            elif tagid == "XXXX":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_4.append([y_int + 0.25, x_int])
            elif tagid == "XXXX":
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
        positions=positions2,
        realtime=None,
        size=0.1,
        fontsize=0,
        color="green",
        lw=1,
        numero=7,
    )
    plt.show()
