"""
Título: Analizador de Estructura de Empleados

Objetivo: Obtener y mostrar un resumen estadístico de la tabla 'employee_master_data'.

Descripción: Este script se conecta a una base de datos PostgreSQL, lee la tabla
de empleados mediante Pandas y genera un análisis descriptivo básico (media,
desviación estándar, etc.) de las columnas numéricas.

Archivo Python: day04_empl_data_analyzer.py

Archivo PNG: day04_empl_data_analyzer.png
"""

# --- IMPORTACIÓN DE LIBRERÍAS ---
# 'pandas' se usa para manipular y analizar los datos (DataFrames).
import pandas as pd
# 'create_engine' permite establecer la conexión con la base de datos SQL.
from sqlalchemy import create_engine
# 'os' sirve para interactuar con el sistema operativo y leer variables de entorno.
import os
# 'load_dotenv' carga las credenciales secretas desde un archivo .env.
from dotenv import load_dotenv

# --- CONFIGURACIÓN Y CONEXIÓN ---
# Carga las variables del archivo .env (DB_USER, DB_PASS, etc.) al entorno actual.
load_dotenv()

# Crea el motor de conexión a PostgreSQL usando las credenciales cargadas.
# Se usa un f-string para formatear la URL de conexión de forma segura.
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- DEFINICIÓN DE FUNCIONES ---
def empl_data_analyzer():
    """
    Función que lee la tabla de empleados y muestra su resumen.
    """
    # 1. Definición de la consulta SQL para extraer columnas específicas de interés. 
    query = """
    SELECT
        age,
        monthly_income,
        job_satisfaction
    FROM
        employee_master_data
    """
    
    # 2. Lee los datos de la base de datos utilizando pandas y la consulta definida.
    # El resultado se almacena en un DataFrame de pandas llamado 'df'.
    df = pd.read_sql(query, con = engine)

    # 3. Muestra en consola un análisis descriptivo (conteo, promedio, min, max, etc.)
    # de las columnas numéricas del DataFrame.
    print(df.describe())

# --- PUNTO DE ENTRADA DEL SCRIPT ---
# Verifica si el script se está ejecutando directamente.
if __name__ == "__main__":
    # Llama a la función principal para ejecutar el análisis.
    empl_data_analyzer()