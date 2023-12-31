#importar librerías
import requests
import pandas as pd
import json
from pandas import json_normalize

#==============Importar archivo .json desde Github======================
def import_json(url):
    '''
    Obtiene un archivo .json de la url indicada y lo convierte en dataframe
    param:: url (string) :ruta del archivo .json
    '''
    # URL cruda del archivo .json
    file_url = url
    
    # Realizar una solicitud GET a la URL cruda del archivo JSON en GitHub
    response = requests.get(file_url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener el contenido del archivo JSON
        data = response.json()
        
        # Crear un DataFrame desde el archivo JSON
        df = pd.json_normalize(data)
        print('archivo obtenido correctamente')
        return df
    else:
        print('No se pudo acceder al archivo en GitHub.')

#===============Procesar archivo .json======================

def convertir_json(df):
    '''
    recibe un dataframe y normaliza las columnas cuyos datos se encuentran en formato json.
    retorna un nuevo dataframe
    param:: df: el dataframe a procesar
    '''

    #convertir arrays a formato plano
    for column in df.columns:
            df = df.explode(column)

    lista_df_normalizado = [] #Lista para alamcenar los df explotados
    for column in df.columns:
            try:
                #Se recorre el df en cada una de sus columnas
                df_normalizado = json_normalize(df[column])
                #Cuando la normalización fue funcional la cantidad de columnas del nuevo df será mayor a 1
                if len(df_normalizado.columns) > 0: 
                    lista_df_normalizado.append(df_normalizado)
                    df = df.drop(columns=column) #Se eliminan las columnas que lograron ser expandidas
            except:
                pass

    df= df.reset_index(drop=True) #eliminar columna index

    for df_new in lista_df_normalizado: 
        df = pd.concat([df,df_new], axis=1)

    return df


# Función para identificar listas de diccionarios en una columna específica
def contiene_lista_de_diccionarios(valor):
    return isinstance(valor, list) and all(isinstance(item, dict) for item in valor)

def conteo_columnas(df):
    # Contar cuántas columnas tienen listas de diccionarios
    conteo = df.applymap(contiene_lista_de_diccionarios).sum()
    return conteo[:].sum()

def ciclo(df):
    # Realizar iteración mientras se cumpla la condición
    while conteo_columnas(df) > 0:
        df = convertir_json(df)
    return df