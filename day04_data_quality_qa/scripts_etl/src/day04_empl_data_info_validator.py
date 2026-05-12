"""
Título: Validador de Estructura de Base de Datos

Objetivo: Verificar la carga y estructura de la tabla 'employee_master_data'.

Descripción: Este script se conecta a una base de datos PostgreSQL, lee la tabla
de empleados y muestra información técnica (columnas, tipos de datos, nulos)
para asegurar que la estructura sea correcta tras una carga de datos.

Archivo Pyhton: day04_empl_data_info_validator.py

Archivo PNG: day04_empl_data_info_validator.png
"""

# --- IMPORTACIÓN DE LIBRERÍAS ---
# 'pandas' se usa para manejar los datos en tablas (DataFrames)
import pandas as pd
# 'create_engine' permite establecer la conexión con la base de datos
from sqlalchemy import create_engine
# 'os' sirve para leer las variables de entorno del sistema
import os
# 'load_dotenv' carga las credenciales ocultas desde un archivo .env
from dotenv import load_dotenv

# Carga las variables de entorno (usuario, contraseña, host) desde el archivo .env
load_dotenv()

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Crea el motor de conexión a PostgreSQL usando las credenciales seguras definidas en el .env
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- DEFINICIÓN DE FUNCIONES ---
def validate_db_structure():
    """Lee la tabla de empleados y muestra su estructura técnica."""
    
    # 1. Lee la tabla 'employee_master_data' de la BD y la guarda en un DataFrame (df)
    df = pd.read_sql("SELECT * FROM employee_master_data", con=engine)
    
    # 2. Muestra información detallada: número de filas, columnas, tipos de datos y uso de memoria
    df.info()

# --- EJECUCIÓN PRINCIPAL ---
# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    # Llama a la función para validar la estructura
    validate_db_structure()