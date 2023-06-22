import sys, os

sys.path.append(os.getcwd())

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import paho.mqtt.client as mqtt
from tkinter import messagebox as MessageBox
from functools import partial

from common.tracking_utils_entero_Canasta import BasketballCourt

from tools_heatmap import mapacalor

from lectura_txt import lectura

# PREGUNTAR por SLIDER con STOP CAP DATA y por qué archivos.txt meter en la carpeta DATA


class Interface:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
        self.fig.subplots_adjust(left=0, bottom=0)
        self.pista = BasketballCourt()
        self.pista.draw(self.ax, grid_step=1)
        self.pista.draw_anclas(self.ax)
        plt.get_current_fig_manager().full_screen_toggle()
        self.button = None
        self.button_cap = None
        self.client_mqtt = None

    def close(self, event):
        plt.close("all")

    def maximize(self, event):
        self.button = "MAXIMIZE"
        plt.get_current_fig_manager().full_screen_toggle()

    def on_message(self, client_sus, userdata, message):
        message_received = str(message.payload.decode("utf-8"))
        tagid, x, y, tiempo = message_received.split(",")
        x_int = float(x)
        y_int = float(y)
        if tagid == "C684":
            self.position_x = y_int + 0.25
            self.position_y = x_int
            self.positions[0].append([y_int + 0.25, x_int])
            self.id = 1
        elif tagid == "9092":
            self.position_x = y_int + 0.25
            self.position_y = x_int
            self.positions[1].append([y_int + 0.25, x_int])
            self.id = 2
        elif tagid == "92AB":
            self.position_x = y_int + 0.25
            self.position_y = x_int
            self.positions[2].append([y_int + 0.25, x_int])
            self.id = 3
        elif tagid == "C70B":
            self.position_x = y_int + 0.25
            self.position_y = x_int
            self.positions[3].append([y_int + 0.25, x_int])
            self.id = 4
        elif tagid == "C9B0":
            self.position_x = y_int + 0.25
            self.position_y = x_int
            self.positions[4].append([y_int + 0.25, x_int])
            self.id = 5

        self.pista.draw_players_realtime(
            ax=None,
            posicion_x=self.position_x,
            posicion_y=self.position_y,
            numero=self.id,
            realtime=True,
            size=0.3,
            fontsize=7,
            edgecolor="white",
            facecolor="green",
            lw=1,
        )

    def capdata(self, event):
        self.button_cap = True
        self.position_x = None
        self.position_y = None
        self.positions = [[], [], [], [], []]

        self.client_mqtt = mqtt.Client("Suscriptor")
        self.client_mqtt.on_message = self.on_message
        self.client_mqtt.connect("127.0.0.1")
        self.client_mqtt.loop_start()
        topic = "PosicionJugadores"
        self.client_mqtt.subscribe(topic)

        # TRATAMIENTO DE ESOS DATOS
        ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
        self.pista.draw(ax, grid_step=1)
        self.pista.draw_anclas(ax)

    def stopcapdata(self, event):
        self.button = "STOP DATA"
        self.client_mqtt.loop_stop()
        self.client_mqtt.disconnect()

    def open(self, event):
        self.button = "OPEN"
        self.archivotxt, self.positions = lectura()

    def tracking(self, event):
        if self.button == "OPEN" or self.button == "HEAT MAP":
            self.button = "TRACKING"
            ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
            self.pista.draw(ax, grid_step=1)
            self.pista.draw_anclas(ax)
            # Por defecto grafica las posiciones del jugador 1
            self.pista.draw_players(
                ax=ax,
                positions=self.positions[0],
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
            # Por defecto muestra el mapa de calor del jugador 1
            data = mapacalor(self.positions[0])
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
            self.pista.draw_white(ax, grid_step=None)
            plt.show()

        else:
            MessageBox.showinfo("Info", "Select a file previously")

    def player(self, id, event):
        if self.button == "OPEN":
            MessageBox.showinfo("Info", "Select a visualization option:\n- Tracking\n- Heat Map")
        elif self.button == "TRACKING":
            ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
            self.pista.draw(ax, grid_step=1)
            self.pista.draw_anclas(ax)
            self.pista.draw_players(
                ax=ax,
                positions=self.positions[id - 1],
                realtime=None,
                size=0.1,
                fontsize=2,
                color="green",
                lw=1,
                numero=id,
            )
            plt.draw()
        elif self.button == "HEAT MAP":
            data = mapacalor(self.positions[id - 1])
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
            self.pista.draw_white(ax, grid_step=None)
            plt.show()
        else:
            MessageBox.showinfo("Info", "Select a file previously")

    # The function to be called anytime a slider's value change
    def update(self, val):
        if self.button == "STOP DATA" or self.button == "TRACKING":
            interval_slider = 100
            ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
            self.pista.draw(ax, grid_step=1)
            self.pista.draw_anclas(ax)
            for id, player in enumerate(self.positions):
                num_positions_player = len(player)
                if num_positions_player != 0:
                    position_list_player = num_positions_player * (val + 100) // interval_slider
                    self.pista.draw_players_realtime(
                        ax=None,
                        posicion_x=player[position_list_player][0],
                        posicion_y=player[position_list_player][1],
                        numero=id + 1,
                        realtime=True,
                        size=0.3,
                        fontsize=7,
                        edgecolor="white",
                        facecolor="green",
                        lw=1,
                    )

        else:
            MessageBox.showinfo("Info", "Select STOP CAP DATA or TRACKING previously")

        self.fig.canvas.draw_idle()

    def reset(self, event):
        self.time_slider.reset()

    def run(self):
        # BUTTONS
        axclose = self.fig.add_axes([0.96, 0.96, 0.03, 0.03])
        bclose = Button(axclose, "X", color="white", hovercolor="red")
        bclose.on_clicked(self.close)

        axmaximize = self.fig.add_axes([0.93, 0.96, 0.03, 0.03])
        bmaximize = Button(axmaximize, "[ ]", color="white")
        bmaximize.on_clicked(self.maximize)

        axcapdata = self.fig.add_axes([0.9, 0.8, 0.1, 0.08])
        bcapdata = Button(axcapdata, "CAPTURE DATA", hovercolor="green")
        bcapdata.on_clicked(self.capdata)

        axstopcapdata = self.fig.add_axes([0.9, 0.74, 0.1, 0.06])
        bstopcapdata = Button(axstopcapdata, "STOP CAP DATA", hovercolor="firebrick")
        bstopcapdata.on_clicked(self.stopcapdata)

        axopen = self.fig.add_axes([0.9, 0.62, 0.1, 0.08])
        bopen = Button(axopen, "OPEN FILE", hovercolor="green")
        bopen.on_clicked(self.open)

        axtracking = self.fig.add_axes([0.9, 0.54, 0.1, 0.08])
        btracking = Button(axtracking, "TRACKING", hovercolor="green")
        btracking.on_clicked(self.tracking)

        axheatmap = self.fig.add_axes([0.9, 0.46, 0.1, 0.08])
        bheatmap = Button(axheatmap, "HEAT MAP", hovercolor="green")
        bheatmap.on_clicked(self.heatmap)

        axplayer1 = self.fig.add_axes([0.9, 0.33, 0.1, 0.08])
        bplayer1 = Button(axplayer1, "PLAYER 1", color="white", hovercolor="green")
        bplayer1.on_clicked(partial(self.player, 1))

        axplayer2 = self.fig.add_axes([0.9, 0.25, 0.1, 0.08])
        bplayer2 = Button(axplayer2, "PLAYER 2", color="white", hovercolor="green")
        bplayer2.on_clicked(partial(self.player, 2))

        axplayer3 = self.fig.add_axes([0.9, 0.17, 0.1, 0.08])
        bplayer3 = Button(axplayer3, "PLAYER 3", color="white", hovercolor="green")
        bplayer3.on_clicked(partial(self.player, 3))

        axplayer4 = self.fig.add_axes([0.9, 0.09, 0.1, 0.08])
        bplayer4 = Button(axplayer4, "PLAYER 4", color="white", hovercolor="green")
        bplayer4.on_clicked(partial(self.player, 4))

        axplayer5 = self.fig.add_axes([0.9, 0.01, 0.1, 0.08])
        bplayer5 = Button(axplayer5, "PLAYER 5", color="white", hovercolor="green")
        bplayer5.on_clicked(partial(self.player, 5))

        # SLIDER
        axtime = self.fig.add_axes([0.12, 0.9, 0.5, 0.03])
        self.time_slider = Slider(
            ax=axtime,
            label="Time",
            valmin=-100,
            valmax=0,
            valinit=0,
            valstep=1,
            initcolor="green",
            track_color="lightgrey",
            handle_style={"facecolor": "black", "edgecolor": "white"},
        )

        self.time_slider.on_changed(self.update)

        resetax = self.fig.add_axes([0.014, 0.895, 0.04, 0.04])
        button = Button(resetax, "RESET", hovercolor="0.975")
        button.on_clicked(self.reset)

        plt.show()


if __name__ == "__main__":
    interfaz = Interface()
    interfaz.run()
