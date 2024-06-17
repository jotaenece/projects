#!/usr/bin/env python3
# python3 ./api_test.py -v


import numpy as np
import pandas as pd
import requests
import psycopg2
import json

from datetime import datetime
from sqlalchemy import create_engine

# Define la ruta completa al archivo de configuración
ruta_al_archivo = 'C:/Users/JorgeNavarro/Documents/projects/config/config.json'

# Lee las credenciales desde el archivo de configuración
with open(ruta_al_archivo, 'r') as config_file:
    config = json.load(config_file)

# Acceder a las credenciales
db_host = config['postgres']['host']
db_database = config['postgres']['database']
db_user = config['postgres']['user']
db_password = config['postgres']['password']


# get data from api
url = 'http://universities.hipolabs.com/search?country=United+States'
response = requests.get(url)
data = response.json()

# convert data to pandas dataframe
df = pd.DataFrame(data)
print(df.head())


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

# Realiza operaciones en la base de datos aquí
engine = create_engine(
    f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}/{connection_params['database']}"
)
    
df.to_sql('usa_universities', engine, if_exists='replace', index=False)

# Cierra la conexión cuando hayas terminado
conn.close()