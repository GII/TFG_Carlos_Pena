# Manual de usuario de la interfaz gráfica
Manual de usuario para la comprensión de las diferentes opciones proporcionadas en la interfaz gráfica y la correcta instalación de los paquetes necesarios para la utilización del código.

Con el objetivo principal de exponer los resultados de forma clara y comprensible para cualquier usuario, se desarrolla una interfaz que se ejecuta con el programa **ranges_pista_con_read_txt_interfaz_grafica.py** y que presenta las opciones detalladas a continuación.

## Captura, almacenamiento y visualización de datos en tiempo real
La opción “CAPTURE DATA” permite no sólo leer y guardar los datos de las distintas posiciones ocupadas por el jugador/es en cada instante en tiempo real en un archivo de texto, sino que también permite la visualización simultánea de cada una de esas posiciones en pista.

Este procedimiento se realiza mediante dos programas independientes y que se han de ejecutar en dos terminales diferentes. El programa **ranges_pista.py** captura, almacena y publica en un topic de MQTT los datos, a la vez que guarda estos mismos datos del posicionamiento en un archivo de texto para poder disponer de ellos desde la opción “OPEN FILE”. Mientras que el programa que ejecuta la interfaz, **ranges_pista_con_read_txt_interfaz_grafica.py**, se suscribe al topic correspondiente y se encarga de la lectura y tratamiento de los datos para posteriormente graficarlos a pista completa. Dado que esta opción del programa sólo graficará la última posición obtenida de cada jugador, esta visualización en tiempo real mostrará las distintas posiciones de los cinco jugadores a la vez en cancha, y no las posiciones de cada jugador por separado en distintos gráficos.

![image](https://github.com/GII/TFG_Carlos_Pena/assets/119660695/5e3c46b4-0b55-4cd0-a602-8a282b1bce92)

## Visualización de datos a través de un archivo.txt
A través de la opción “OPEN FILE”, el programa permite visualizar la trayectoria realizada por el jugador en el tiempo con la opción “TRACKING”, a partir de la lectura de un archivo de texto previamente seleccionado. La interfaz no sólo permite visualizar la posición de un jugador, sino que el usuario podrá elegir qué trayectoria de los 5 jugadores en pista desea analizar, mediante los botones de “PLAYER 1”, “PLAYER 2”, “PLAYER 3”,  “PLAYER 4” y “PLAYER 5” situados en la parte inferior derecha de la interfaz gráfica.

![image](https://github.com/GII/TFG_Carlos_Pena/assets/119660695/708ebb6a-a76a-4d72-9b38-10c7d9aa2fbc)

Esta opción permite también la generación de un mapa de calor, individual para cada jugador, al pulsar la opción “HEAT MAP”.

![image](https://github.com/GII/TFG_Carlos_Pena/assets/119660695/73fd456e-cfc5-4fa3-b15b-7f16b99458e4)

## Barra interactiva
La barra interactiva o slider permite, tanto en la opción de tracking como en la opción de visualización de las posiciones en tiempo real, situarse de forma manual en el instante de tiempo deseado por el usuario/entrenador. En función de la variación de la variable tiempo, esta opción permite al entrenador manejar de forma interactiva la progresión, a la velocidad deseada, de las distintas posiciones ocupadas por los cinco jugadores en cada instante de la jugada y centrar la atención en el momento que considere más relevante.

Para aplicar esta funcionalidad se ha de seleccionar la opción de lectura y graficado de las posiciones en tiempo real “CAPTURE DATA”, y cuando se desee parar la recogida de datos y manejar manualmente las posiciones previamente obtenidas, se ha de presionar el botón “STOP CAP DATA”. También es posible disponer de la barra interactiva en el seguimiento de las posiciones de los jugadores a través de los datos obtenidos de un archivo.txt, presionando la opción de “TRACKING”. Tras haber seleccionado cualquiera de las dos opciones, estará disponible la funcionalidad interactiva del slider recogiendo y graficando los datos de posición de los cincos jugadores en pista en función del valor de la barra escogido por el usuario/entrenador.

![image](https://github.com/GII/TFG_Carlos_Pena/assets/119660695/b94488a0-c947-41d4-b604-01412376ac6b)

## Librerías utilizadas
Con la finalidad de facilitar la descarga de los programas necesarios para correr, en Visual Studio Code, el archivo.py que ejecuta la interfaz gráfica, se detallan las librerías que se han de instalar:
- Para la visualización de los resultados en pista se utiliza la librería matplotlib. A partir de ella se desarrollan funciones para representar la cancha de baloncesto completa, el posicionamiento de las anclas y las sucesivas posiciones que fue ocupando el jugador, definidas por las coordenadas x e y a lo largo del tiempo.
- Para la utilización de los botones interactivos que permiten seleccionar las distintas opciones del programa se importa de matplotlib.widgets la clase Button dentro de la propia librería matplotlib. De widgets se importa también la clase Slider que nos permite el uso de la barra interactiva para controlar y manejar la visualización de las distintas posiciones en función de la variable tiempo.
- Para el mapa de calor se desarrolla una función que procese la cantidad de veces que han sido ocupadas las distintas zonas en las que dividimos la cancha. Estos datos se representan en un mapa de calor generado por la función imshow() también perteneciente a la librería matplotlib.
- Las ventanas emergentes que muestran mensajes de información, advertencia o error se han programado a partir de la librería tkinter.
- Por último, se ha de realizar también la instalación de las librerías sys, os, serial, time, math, numpy, paho.mqtt.client y functools que utilizan los diferentes programas que conforman la interfaz gráfica.




