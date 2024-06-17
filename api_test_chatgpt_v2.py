#!/usr/bin/env python3

import numpy as np
import pandas as pd
import requests
import psycopg2
import json
from datetime import datetime
from sqlalchemy import create_engine

# Define la ruta completa al archivo de configuración
ruta_al_archivo = 'C:/Users/JorgeNavarro/Documents/projects/config/config.json'

# Función para obtener datos de la API
def get_data():
    url = 'http://universities.hipolabs.com/search?country=United+States'
    response = requests.get(url)
    data = response.json()
    return data

# Función para normalizar el DataFrame
def normalize_df(df, schema, verbose=False):
    df = df.rename(columns=schema)
    if verbose:
        print("Normalized column names:")
        print(df.columns)
    return df

# Función principal
def main(args):
    # Lee las credenciales desde el archivo de configuración
    with open(ruta_al_archivo, 'r') as config_file:
        config = json.load(config_file)

    # Acceder a las credenciales
    db_host = config['postgres']['host']
    db_database = config['postgres']['database']
    db_user = config['postgres']['user']
    db_password = config['postgres']['password']

    # Especifica los parámetros de conexión, incluyendo el esquema deseado
    connection_params = {
        "host": db_host,
        "database": db_database,
        "user": db_user,
        "password": db_password,
        "options": f"-c search_path=test"
    }

    # Establece la conexión
    conn = psycopg2.connect(**connection_params)
    engine = create_engine(
        f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}/{connection_params['database']}"
    )

    # Define el esquema
    SCHEMA = {
        "state-province": "state-province",
        "alpha_two_code": "alpha_two_code",
        "domains": "domains",
        "name": "name",
        "country": "country",
        "web_pages": "web_pages",
        "timestamp_ejecucion": "timestamp_ejecucion",
        "year": "year",
        "date": "date"
        # Agrega más columnas según sea necesario
    }

    # Calcula el timestamp de ejecución del script
    timestamp_ejecucion = pd.Timestamp.now()

    # Obtiene los datos de la API
    data = get_data()

    # Convierte los datos a un DataFrame
    df = pd.DataFrame(data)
    df.columns = df.columns.str.lower()

    # Agrega la columna con el timestamp de ejecución
    df["timestamp_ejecucion"] = timestamp_ejecucion

    # Agrega las columnas de year y date
    df["year"] = timestamp_ejecucion.year
    df["date"] = timestamp_ejecucion.date

    # Normaliza el DataFrame
    df = normalize_df(df, SCHEMA, args.verbose)

    # Guarda el DataFrame en la base de datos
    df.to_sql('usa_universities', engine, if_exists='replace', index=False)

    # Cierra la conexión cuando hayas terminado
    conn.close()

if __name__ == "__main__":
    # Define argumentos y opciones según sea necesario
    import argparse

    parser = argparse.ArgumentParser(description='Descripción de tu script')
    parser.add_argument('-v', '--verbose', action='store_true', help='Mostrar mensajes de depuración')
    parser.add_argument('--fromdate', type=str, help='Fecha de inicio')
    parser.add_argument('--todate', type=str, help='Fecha de fin')

    args = parser.parse_args()
    main(args)
