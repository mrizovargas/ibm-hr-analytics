# ---------------------------------------------------------------------------
# Título: Análisis de Cardinalidad en Datos Maestros de Empleados
# 
# Objetivo: Analizar la cantidad de valores únicos (cardinalidad) en columnas 
# clave de la tabla 'employee_master_data' para entender la diversidad de los 
# datos.
# 
# Descripción: El script se conecta a una base de datos PostgreSQL, extrae la 
# información maestra de empleados y calcula cuántos valores distintos existen 
# en columnas específicas (departamento, satisfacción, rotación) para evaluar 
# la calidad y distribución de la información.
# 
# Archivo Python: day04_empl_data_unique_analysis.py
# 
# Archivo PNG: day04_empl_data_unique_analysis.png
# ---------------------------------------------------------------------------

# --- IMPORTACIÓN DE LIBRERÍAS ---
# 'pandas' para manipulación y análisis de datos.
import pandas as pd
# 'create_engine' para gestionar la conexión a la base de datos SQL.
from sqlalchemy import create_engine
# 'os' para interactuar con el sistema operativo y leer variables de entorno.
import os
# 'load_dotenv' para cargar credenciales de forma segura desde un archivo .env.
from dotenv import load_dotenv

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Carga las variables de entorno (usuario, pass, host, etc.) del archivo .env
load_dotenv()

# Crea el "motor" de conexión a PostgreSQL usando las credenciales cargadas
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- DEFINICIÓN DE CONSULTA ---
# Sentencia SQL para seleccionar todos los datos de la tabla de empleados
query = """
    SELECT *
    FROM
        employee_master_data
"""

# --- FUNCIÓN PRINCIPAL DE ANÁLISIS ---
def empl_data_unique_analysis():
    """
    Lee los datos de la BD y muestra el conteo de valores únicos por columna.
    """
    
    # Ejecuta la consulta SQL y carga el resultado en un DataFrame de Pandas
    df = pd.read_sql(query, con = engine)

    # Imprime la cantidad de valores únicos para todas las columnas de la tabla
    print("\n---- Valores Únicos por Columna ----")
    print(df.nunique())

    # Cuenta cuántos departamentos distintos existen
    print("\n---- Valores Únicos por Departamento ----")
    print(df['department'].nunique())

    # Cuenta la satisfacción laboral, incluyendo valores nulos (sin eliminar vacíos)
    print("\n---- Valores Únicos de Satisfacción con nulos ----")
    print(df['job_satisfaction'].nunique(dropna = False))

    # Cuenta valores distintos en la columna de rotación (Attrition)
    print("\n---- Valores Únicos en Attrition ----")
    print(df['attrition'].nunique())

    print("\n")

# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    # Llama a la función de análisis solo si el script se ejecuta directamente
    empl_data_unique_analysis()