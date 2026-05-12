# -------------------------------------------------------------------------------
# Título: Detección de Tarifas Diarias Atípicas
# 
# Objetivo: Identificar empleados con tarifas diarias fuera del rango lógico.
# 
# Descripción: Este script consulta los datos maestros de empleados desde una base 
# de datos PostgreSQL, filtra aquellos cuya 'daily_rate' sea menor a 100 o mayor a 
# 1500, y muestra el total de registros atípicos encontrados.
# 
# Archivo Python: day04_daily_rate_outliers_02.py
# 
# Archivo PNG: day04_daily_rate_outliers_02.png
# -------------------------------------------------------------------------------

# Biblioteca para manipulación y análisis de datos
import pandas as pd
# Módulo para conectar con la base de datos
from sqlalchemy import create_engine
# Módulo para leer variables de entorno del sistema
import os
# Carga variables desde un archivo .env
from dotenv import load_dotenv

# --- Configuración Inicial ---
# Carga las credenciales de la base de datos (host, usuario, contraseña, etc.)
load_dotenv()

# Crea la conexión a PostgreSQL usando las credenciales cargadas
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Consulta SQL para traer todos los datos de empleados
query = """
    SELECT *
    FROM
        employee_master_dirty_data
"""

# Función principal para leer datos y detectar anomalías en la tarifa diaria.
def daily_rate_outliers():
    try:
        # Intenta cargar los datos de la base de datos a un DataFrame de Pandas
        df = pd.read_sql(query, con = engine)
    except Exception as e:
        # Si la conexión falla, muestra un mensaje de error detallado
        print(f"❌ Error al conectarse al dataset: {e}")
        return
    
    # Filtra el DataFrame buscando tarifas diarias menores a 100 o mayores a 1500
    outliers = df[(df['daily_rate'] < 100) | (df['daily_rate'] > 1500)]

    # Muestra los resultados en consola
    print("\n---- Registros Fuera de Rango ----")
    print(f"Total de registros con tarifa atípica: {len(outliers)}")
    print("\n")

# --- Ejecución del Script ---
if __name__ == "__main__":
    # Llama a la función si el script se ejecuta directamente
    daily_rate_outliers()