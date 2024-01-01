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

    lista_df_normalizado = [] #Lista para almacenar el df expandido
    for column in df.columns:
            try:
                #Se recorre el df en cada una de sus columnas
                df_normalizado = json_normalize(df[column])
                #Cuando la normalización fue funcional la cantidad de columnas del nuevo df será mayor a 0
                if len(df_normalizado.columns) > 0: 
                    lista_df_normalizado.append(df_normalizado)
                    df = df.drop(columns=column) #Se eliminan las columnas que lograron ser expandidas
            except Exception as e:
                print(f"Error al normalizar la columna '{column}': {e}")

    df= df.reset_index(drop=True) #eliminar columna index

    for df_new in lista_df_normalizado: 
        df = pd.concat([df,df_new], axis=1)

    return df


# =========Identificar columnas que aún presentan formato de lista de diccionarios===========

def contiene_lista_de_diccionarios(valor):
    '''
    Verifica si un valor es una lista de diccionarios.
    Retorna True si el valor proporcionado es una lista y todos sus elementos son diccionarios.
    param:: valor: elemento a evaluar
    '''
    #Verificar si el valor dado es una lista.
    #Para cada item en la lista, isinstance(item, dict) verifica si ese elemento es un diccionario.
    return isinstance(valor, list) and all(isinstance(item, dict) for item in valor)

def conteo_columnas(df):
    '''
    Aplica la función "contiene_lista_de_diccionarios" a cada columna del dataframe
    Cuenta cuántas columnas del dataframe 'df' contienen listas de diccionarios
    Retorna la cantidad de columnas que cumplen con la condición
    param:: df: dataframe a evaluar
    '''
    conteo = df.applymap(contiene_lista_de_diccionarios).sum() #usar .map en versiones de pandas >= 2.1.0
    return conteo[:].sum()

def normalizar_json(df):
    '''
    Itera continuamente hasta que no existan columnas que contengan listas de diccionarios en el dataframe.
    Utiliza conteo_columnas(df) para verificar si aún existen columnas con listas de diccionarios.
    Llama a la función convertir_json(df) para normalizar los datos.
    param:: df: dataframe a evaluar
    '''
    # Realizar iteración mientras se cumpla la condición
    while conteo_columnas(df) > 0:
        df = convertir_json(df)
    return df