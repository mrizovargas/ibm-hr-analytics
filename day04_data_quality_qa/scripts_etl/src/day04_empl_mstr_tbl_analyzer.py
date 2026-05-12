# ----------------------------------------------------------------------------------
# Título: Extractor y Analizador de Dimensiones de Tabla Maestra de Empleados
# 
# Objetivo: Conectarse a una base de datos PostgreSQL, extraer la tabla maestra de 
# empleados y mostrar cuántas filas y columnas (dimensiones) tiene.
# 
# Descripción: Este script automatiza la carga de datos desde una base de datos 
# segura (usando variables de entorno) y utiliza Pandas para gestionar la información, 
# permitiendo validar rápidamente la estructura de la tabla.
# 
# Archivo Python: day04_empl_mstr_tbl_analyzer.py
# 
# Archivo PNG: day04_empl_mstr_tbl_analyzer.png
# ----------------------------------------------------------------------------------

# Importación de librerías necesarias
import pandas as pd  # Para manejo y análisis de datos (DataFrames)
from sqlalchemy import create_engine  # Para establecer la conexión a SQL
import os  # Para interactuar con el sistema operativo y leer variables de entorno
from dotenv import load_dotenv  # Para cargar credenciales seguras desde un archivo .env

# --- CONFIGURACIÓN Y CONEXIÓN ---
# Carga las variables de entorno (DB_USER, DB_PASS, etc.) del archivo .env
load_dotenv()

# Crea el motor de conexión a PostgreSQL usando las credenciales seguras
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- EXTRACCIÓN DE DATOS ---
# Define la consulta SQL para obtener toda la información
query = """
    SELECT * 
    FROM 
        employee_master_data
"""

# Ejecuta la consulta y carga los datos en un DataFrame de Pandas
df = pd.read_sql(query, con = engine)

# --- FUNCIÓN DE ANÁLISIS ---
def empl_mstr_tbl_analyzer():
    """
    Función que imprime las dimensiones (filas, columnas) del DataFrame.
    """
    print("\n---- Dimensiones Tabla Maestra de Empleados ----")
    # df.shape devuelve una tupla (n_filas, n_columnas)
    print(df.shape)
    print("\n")

# --- EJECUCIÓN DEL SCRIPT ---
# Punto de entrada principal: verifica si el script se ejecuta directamente
if __name__ == "__main__":
    # Llama a la función para mostrar las dimensiones
    empl_mstr_tbl_analyzer()