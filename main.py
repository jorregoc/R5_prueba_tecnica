from functions import *

#url del archivo en github
url = 'https://raw.githubusercontent.com/jorregoc/R5_prueba_tecnica/main/data_raw/taylor_swift_spotify.json'


df = import_json(url) #importar archivo .json
df_final = ciclo(df) # procesar archivo

df_final.to_csv('dataset.csv', index=False) #exportar archivo a .csv