import sys, os

sys.path.append(os.getcwd())

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import paho.mqtt.client as mqtt
from tkinter import messagebox as MessageBox
from functools import partial
from lectura_datos import ranges_pista


# https://docs.hektorprofe.net/python/interfaces-graficas-con-tkinter/dialogs-dialogos/

from common.tracking_utils_entero_Canasta import (
    draw_court,
    draw_court_white,
    draw_anclas,
    draw_players,
)
from tools_heatmap import mapacalor, lectura_mp

from lectura_txt import lectura

"""
AVANZAR EN:
- Botones de Capture data y Stop --> demo.run() --> while stopcapdata != "STOP DATA" usar esa variable
- Guardar los botones presionados previamente en variables
- Barra en función del tiempo --> update cuando no es una variable de la gráfica
- Mapa de calor delimitando zonas

-Posible mejora de rapidez en la interfaz
"""


# INTERFAZ GRÁFICA


class Index:
    def __init__(self):
        self.button = None
        '''self.client_sus = mqtt.Client("Suscriptor")
        # conectarse al broker MQTT en la dirección IP del GII
        self.client_sus.connect("10.8.20.145")
        self.topic = "Prueba"'''

    def close(self, event):
        self.button = "CLOSE"
        plt.close("all")

    def maximize(self, event):
        self.button = "MAXIMIZE"
        plt.get_current_fig_manager().full_screen_toggle()

    def capdata(self, event):
        self.button = "CAPTURE DATA"
        # self.client_sus.subscribe(self.topic)
        # TRATAMIENTO DE ESOS DATOS
        ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))

        # AL PULSAR EN CAP DATA QUE APAREZCA STOP DATA Y A SU VEZ AL PULSAR EN ESTE QUE APAREZCA CONTINUE
        ax.set_visible(bstopcapdata)

    def stopcapdata(self, event):
        self.button = "STOP DATA"

    def continuecapdata(self, event):
        self.button = "CONTINUE DATA"

    def open(self, event):
        self.button = "OPEN"
        (
            self.archivotxt,
            self.positions1,
            self.positions2,
            self.positions3,
            self.positions4,
            self.positions5,
        ) = lectura()

    def tracking(self, event):
        if self.button == "OPEN" or self.button == "HEAT MAP":
            self.button = "TRACKING"
            ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
            draw_court(ax, grid_step=1)
            draw_anclas(ax)
            # Por defecto grafica las posiciones del jugador 1
            draw_players(
                ax=ax,
                positions=self.positions1,
                realtime=None,
                size=0.1,
                fontsize=2,
                color="green",
                lw=1,
                numero=1,
            )
        else:
            MessageBox.showinfo("Info", "Select a file previously")

    def heatmap(self, event):
        if self.button == "OPEN" or self.button == "TRACKING":
            self.button = "HEAT MAP"
            (
                self.positions1_mp,
                self.positions2_mp,
                self.positions3_mp,
                self.positions4_mp,
                self.positions5_mp,
            ) = lectura_mp(self.archivotxt)
            # Por defecto muestra el mapa de calor del jugador 1
            data = mapacalor(self.positions1_mp)
            ax = plt.axes(xlim=(0, 32), ylim=(0, 19))
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
            draw_court_white(ax, grid_step=None)
            plt.show()

        else:
            MessageBox.showinfo("Info", "Select a file previously")

    def player(self, id, event):
        if id == 1:
            positions = self.positions1
            positions_mp = self.positions1_mp
        elif id == 2:
            positions = self.positions2
            positions_mp = self.positions2_mp
        elif id == 3:
            positions = self.positions3
            positions_mp = self.positions3_mp
        elif id == 4:
            positions = self.positions4
            positions_mp = self.positions4_mp
        elif id == 5:
            positions = self.positions5
            positions_mp = self.positions5_mp
        if self.button == "OPEN":
            MessageBox.showinfo("Info", "Select a visualization option:\n- Tracking\n- Heat Map")
        elif self.button == "TRACKING":
            ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
            draw_court(ax, grid_step=1)
            draw_anclas(ax)
            draw_players(
                ax=ax,
                positions=positions,
                realtime=None,
                size=0.1,
                fontsize=2,
                color="green",
                lw=1,
                numero=1,
            )
            plt.draw()
        elif self.button == "HEAT MAP":
            data = mapacalor(positions_mp)
            ax = plt.axes(xlim=(0, 32), ylim=(0, 19))
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
            draw_court_white(ax, grid_step=None)
            plt.show()
        else:
            MessageBox.showinfo("Info", "Select a file previously")


class Interface:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
        self.fig.subplots_adjust(left=0, bottom=0)
        draw_court(self.ax, grid_step=1)
        draw_anclas(self.ax)
        plt.get_current_fig_manager().full_screen_toggle()

    def run(self):
        callback = Index()
        # BUTTONS
        axclose = self.fig.add_axes([0.96, 0.96, 0.03, 0.03])
        bclose = Button(axclose, "X", color="white", hovercolor="red")
        bclose.on_clicked(callback.close)

        axmaximize = self.fig.add_axes([0.93, 0.96, 0.03, 0.03])
        bmaximize = Button(axmaximize, "[ ]", color="white")
        bmaximize.on_clicked(callback.maximize)

        axcontinuecapdata = self.fig.add_axes([0.9, 0.8, 0.1, 0.08])
        bcontinuecapdata = Button(axcontinuecapdata, "STOP", color="red", hovercolor="firebrick")
        bcontinuecapdata.on_clicked(callback.continuecapdata)

        axstopcapdata = self.fig.add_axes([0.9, 0.8, 0.1, 0.08])
        bstopcapdata = Button(axstopcapdata, "STOP", color="red", hovercolor="firebrick")
        bstopcapdata.on_clicked(callback.stopcapdata)

        axcapdata = self.fig.add_axes([0.9, 0.8, 0.1, 0.08])
        bcapdata = Button(axcapdata, "CAPTURE DATA", hovercolor="green")
        bcapdata.on_clicked(callback.capdata)

        axopen = self.fig.add_axes([0.9, 0.72, 0.1, 0.08])
        bopen = Button(axopen, "OPEN FILE", hovercolor="green")
        bopen.on_clicked(callback.open)

        axtracking = self.fig.add_axes([0.9, 0.64, 0.1, 0.08])
        btracking = Button(axtracking, "TRACKING", hovercolor="green")
        btracking.on_clicked(callback.tracking)

        axheatmap = self.fig.add_axes([0.9, 0.56, 0.1, 0.08])
        bheatmap = Button(axheatmap, "HEAT MAP", hovercolor="green")
        bheatmap.on_clicked(callback.heatmap)

        axplayer1 = self.fig.add_axes([0.9, 0.33, 0.1, 0.08])
        bplayer1 = Button(axplayer1, "PLAYER 1", color="white", hovercolor="green")
        bplayer1.on_clicked(partial(callback.player, 1))

        axplayer2 = self.fig.add_axes([0.9, 0.25, 0.1, 0.08])
        bplayer2 = Button(axplayer2, "PLAYER 2", color="white", hovercolor="green")
        bplayer2.on_clicked(partial(callback.player, 2))

        axplayer3 = self.fig.add_axes([0.9, 0.17, 0.1, 0.08])
        bplayer3 = Button(axplayer3, "PLAYER 3", color="white", hovercolor="green")
        bplayer3.on_clicked(partial(callback.player, 3))

        axplayer4 = self.fig.add_axes([0.9, 0.09, 0.1, 0.08])
        bplayer4 = Button(axplayer4, "PLAYER 4", color="white", hovercolor="green")
        bplayer4.on_clicked(partial(callback.player, 4))

        axplayer5 = self.fig.add_axes([0.9, 0.01, 0.1, 0.08])
        bplayer5 = Button(axplayer5, "PLAYER 5", color="white", hovercolor="green")
        bplayer5.on_clicked(partial(callback.player, 5))

        # SLIDER https://matplotlib.org/2.0.2/examples/widgets/slider_demo.html  https://matplotlib.org/stable/gallery/widgets/slider_demo.html
        axtime = self.fig.add_axes([0.12, 0.9, 0.5, 0.03])
        time_slider = Slider(
            ax=axtime,
            label="Time [s]",
            valmin=-60,
            valmax=0,
            valinit=0,
            valstep=0.1,
            initcolor="green",
            track_color="lightgrey",
            handle_style={"facecolor": "black", "edgecolor": "white"},
        )

        # The function to be called anytime a slider's value change
        def update(val):
            ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
            draw_court(ax, grid_step=1)
            draw_anclas(ax)
            # Por defecto grafica las posiciones del jugador 1
            draw_players(
                ax=ax,
                positions=self.positions1,
                realtime=None,
                size=0.1,
                fontsize=2,
                color="green",
                lw=1,
                numero=1,
            )
            self.fig.canvas.draw_idle()

        time_slider.on_changed(update)

        resetax = self.fig.add_axes([0.014, 0.895, 0.04, 0.04])
        button = Button(resetax, "RESET", hovercolor="0.975")

        def reset(event):
            time_slider.reset()

        button.on_clicked(reset)
        plt.show()


if __name__ == "__main__":
    interfaz = Interface()
    interfaz.run()