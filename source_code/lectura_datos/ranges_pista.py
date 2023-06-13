import sys, os

sys.path.append(os.getcwd())

import serial, time
from serial import SerialException
import numpy as np
import math
import paho.mqtt.client as mqtt


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
        self.client_pub.connect("127.0.0.1")
        self.client_pub.loop_start()
        self.topic = "PosicionJugadores"

    def run(self):
        # connect to tag via serial port
        try:
            self.ser.close()
            self.ser.open()
            time.sleep(1)
            # configure mdek as a tagn
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

            # read and publish data
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
                    # filtrado NaN
                    if not math.isnan(x_int) and not math.isnan(y_int):
                        with open("PRUEBA.txt", "a") as file:
                            file.write(f"{tagid},{x},{y},{tiempo}\n")
                        # MQTT (publicación)
                        message = f"{tagid},{x},{y},{tiempo}\n"
                        self.client_pub.publish(self.topic, message)

            self.ser.close()
        except SerialException:
            print("Could not connect to the serial port")


if __name__ == "__main__":
    # Activar Servicio Mosquitto Broker
    demo = Ranges()
    demo.run()
