import sys, os

sys.path.append(os.getcwd())

import serial, time
from serial import SerialException
import numpy as np
import paho.mqtt.client as mqtt

from common.tracking_utils_entero_Canasta import draw_court, draw_anclas, draw_players


class Ranges:
    def __init__(self):
        # initialize serial port
        dwPort = "COM9"
        dwRate = 115200
        self.ser = serial.Serial(port=dwPort, timeout=10, baudrate=dwRate)
        # ranges :         rt1,    rt2,    rt3,    rt4,    ra12,   ra13,   ra23,   ra24,   ra34
        self.Z = np.mat([[15.0], [15.0], [15.0], [15.0], [15.0], [15.0], [15.0], [15.0], [15.0]])
        # MQTT
        self.client_pub = mqtt.Client("Publicador")
        # conectarse al broker MQTT en la dirección IP del GII
        self.client_pub.connect("10.8.20.145")
        self.topic = "Prueba"

    def run(self):
        # connect to tag via serial port
        try:
            self.ser.close()
            self.ser.open()
            time.sleep(1)
            # configure mdek as a tag
            self.ser.write(b"nmt\r")
            time.sleep(1)
            self.ser.write(b"\r")
            self.ser.write(b"\r")
            time.sleep(1)
            # set mdek in passive mode
            self.ser.write(b"nmp\r")
            time.sleep(1)
            self.ser.write(b"\r")
            self.ser.write(b"\r")
            time.sleep(1)
            # print ranges through serial port
            self.ser.write(b"lec\r")
            time.sleep(1)
            print("serial connection established")
            tiempo0 = time.time()

            # read, publish and represent data
            archivo = ttk.Entry()

            while True:
                raw_data = self.ser.readline()
                data = raw_data.decode(encoding="ascii", errors="ignore")
                if "POS" in data:
                    _, _, tagid, x, y, z, fiab, _ = data.split(",")
                    tiempo = time.time() - tiempo0
                    # CONDICIÓN PARA QUE NO TRABAJE CON LOS NAN
                    x_int = float(x)  # con el data.split() tenemos strings
                    y_int = float(y)
                    z_int = float(z)
                    print(f"Tag {tagid}: {x_int}, {y_int+0.25}, {z_int}. Tiempo={tiempo}s")
                    """if tagid == "9092":
                        if not math.isnan(x_int) and not math.isnan(
                            y_int
                        ):  # comprueba si los valores son distintos de nan
                            if self.visualizacion_jugadores == 2:
                                # SE BORRA LA PISTA cuando recibo datos si no lo recorro con el debugger
                                draw_players(
                                    posicion_x=y_int + 0.75,
                                    posicion_y=x_int,
                                    numero=1,
                                )  # MODIFICAR Y QUITAR + 4.3
                            elif self.visualizacion_jugadores == 3:
                                draw_players(
                                    posicion_x=y_int + 0.75,
                                    posicion_y=x_int,
                                    numero=1,
                                    realtime="Si",
                                )
                    elif tagid == "XXXX":
                        if not math.isnan(x_int) and not math.isnan(y_int):
                            if self.visualizacion_jugadores == 2:
                                draw_players(
                                    posicion_x=y_int, posicion_y=-x_int, numero=2
                                )
                            elif self.visualizacion_jugadores == 3:
                                draw_players(
                                    posicion_x=y_int + 0.75,
                                    posicion_y=x_int,
                                    numero=2,
                                    realtime="Si",
                                )
                    elif tagid == "XXXX":
                        if not math.isnan(x_int) and not math.isnan(y_int):
                            if self.visualizacion_jugadores == 2:
                                draw_players(
                                    posicion_x=y_int, posicion_y=-x_int, numero=3
                                )
                            elif self.visualizacion_jugadores == 3:
                                draw_players(
                                    posicion_x=y_int + 0.75,
                                    posicion_y=x_int,
                                    numero=3,
                                    realtime="Si",
                                )
                    elif tagid == "XXXX":
                        if not math.isnan(x_int) and not math.isnan(y_int):
                            if self.visualizacion_jugadores == 2:
                                draw_players(
                                    posicion_x=y_int, posicion_y=-x_int, numero=4
                                )
                            elif self.visualizacion_jugadores == 3:
                                draw_players(
                                    posicion_x=y_int + 0.75,
                                    posicion_y=x_int,
                                    numero=4,
                                    realtime="Si",
                                )
                    elif tagid == "XXXX":
                        if not math.isnan(x_int) and not math.isnan(y_int):
                            if self.visualizacion_jugadores == 2:
                                draw_players(
                                    posicion_x=y_int, posicion_y=-x_int, numero=5
                                )
                            elif self.visualizacion_jugadores == 3:
                                draw_players(
                                    posicion_x=y_int + 0.75,
                                    posicion_y=x_int,
                                    numero=5,
                                    realtime="Si",
                                )"""
                    # actualización de la figura
                    with open(archivo, "a") as file:
                        file.write(f"{tagid},{x},{y},{tiempo}\n")
                    # MQTT (publicación)
                    message = f"{tagid},{x},{y},{tiempo}\n"
                    self.client_pub.publish(self.topic, message)
            self.ser.close()
        except SerialException:
            print("Could not connect to the serial port")
        # return positions_P1, positions_P2, positions_P3, positions_P4, positions_P5

        # def cliente_suscriptor(self):
        client_sus = mqtt.Client("Suscriptor")
        # conectarse al broker MQTT en la dirección IP del GII
        client_sus.connect("10.8.20.145")
        client_sus.subscribe("Prueba")
        return client_sus


if __name__ == "__main__":
    demo = Ranges()
    demo.run()
