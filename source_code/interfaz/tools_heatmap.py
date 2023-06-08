import sys, os

sys.path.append(os.getcwd())

import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from tkinter import filedialog as FileDialog
from common.tracking_utils_entero_EI import (
    draw_court,
    draw_anclas,
    draw_players,
)


def lectura_mp(archivotxt):
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
                            x_int + 9.5,
                        ]  # Ajustes a los ejes para TomaDatos_0505 y + 4.3 , -x + 0.8
                    )
            elif tagid == "C684":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_2.append([y_int + 0.25, x_int + 10])
            elif tagid == "XXXX":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_3.append([y_int + 0.25, x_int + 10])
            elif tagid == "XXXX":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_4.append([y_int + 0.25, x_int + 10])
            elif tagid == "XXXX":
                if not math.isnan(x_int) and not math.isnan(y_int):
                    positions_5.append([y_int + 0.25, x_int + 10])

    positions_1_dic = {i: v for i, v in enumerate(positions_1)}
    positions_2_dic = {i: v for i, v in enumerate(positions_2)}
    positions_3_dic = {i: v for i, v in enumerate(positions_3)}
    positions_4_dic = {i: v for i, v in enumerate(positions_4)}
    positions_5_dic = {i: v for i, v in enumerate(positions_5)}
    print(positions_2_dic)
    return (
        positions_1_dic,
        positions_2_dic,
        positions_3_dic,
        positions_4_dic,
        positions_5_dic,
    )


def mapacalor(positions):
    data = []
    for i in range(0, 190):
        data.append([])
        for j in range(0, 320):
            data[i].append(0)

    number_positions = list(positions.keys())
    positions_xy = list(positions.values())
    for k in number_positions:
        x = positions_xy[k][0]
        y = positions_xy[k][1]
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
    archivo = FileDialog.askopenfilename(title="Abrir un fichero")
    positions1, positions2, positions3, positions4, positions5 = lectura_mp(archivo)
    data = mapacalor(positions2)
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

"""# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(farmers)), labels=farmers)
ax.set_yticks(np.arange(len(vegetables)), labels=vegetables)"""

"""# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")"""

"""# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j], ha="center", va="center", color="w")"""

"""ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()"""