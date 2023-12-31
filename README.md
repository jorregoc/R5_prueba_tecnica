# R5_prueba_tecnica

Este repositorio contiene la solución a la prueba técnica para el cargo de Data Quality Engineer en R5.
La estructura es la siguiente:

El archivo **functions.py** contiene las funciones necesarias para descargar el archivo .json directamente desde el repositorio de Github y normalizarlo mediante el uso de las librerías pandas y json.

El archivo **main.py** importa las funciones del archivo functions.py para descargar el archivo .json, normalizarlo y exporta el resultado como un archivo .csv

**data_raw**:
* taylor_swift_spotify.json: archivo .json con la información a analizar.
* dataset.csv: resultado de procesar la estructura del .json mediante el script main.py

**notebooks**:
* reporte_codigo.ipynb: Notebook con el código y análisis de calidad de los datos

**reporte**:
* Contiene el reporte de calidad de los datos en formato pdf y el código con el cuál se realizó el análisis en formato .html



