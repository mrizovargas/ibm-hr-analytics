# -----------------------------------------------------------------------------------
# Título: Identificador de Empleados con Bajos Ingresos
# 
# Objetivo: Detectar y listar empleados cuyo ingreso mensual es atípicamente bajo.
# 
# Descripción: Este script se conecta a una base de datos PostgreSQL, extrae información
# de empleados y filtra aquellos con un 'monthly_income' menor a 1500 para
# su revisión.
# 
# Archivo Python: day04_analyze_data_low_income_02.py
# 
# Archivo PNG: day04_analyze_data_low_income_02.png
# -----------------------------------------------------------------------------------

# Importa la librería para manejo de datos (DataFrames)
import pandas as pd
# Para gestionar la conexión a la BD
from sqlalchemy import create_engine
# Para leer variables de entorno del sistema
import os
# Para cargar credenciales desde un archivo .env
from dotenv import load_dotenv

# 1. Configuración de conexión
load_dotenv()  # Carga las credenciales (host, usuario, pass) ocultas en el archivo .env

# Crea el motor de conexión a PostgreSQL usando las variables de entorno
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# 2. Definición de la consulta SQL
# Selecciona toda la información de la tabla maestra de empleados
query = """
    SELECT *
    FROM
        employee_master_dirty_data
"""

# 3. Función principal para extraer y analizar datos
def data_low_income():
    try:
        # Intenta leer la base de datos y cargarla en un DataFrame de Pandas
        df = pd.read_sql(query, con=engine)
    except Exception as e:
        # Si hay error (conexión, permisos), lo muestra y detiene la función
        print(f"❌ Error al conectarse al dataset: {e}")
        return
    
    # --- PROCESAMIENTO DE DATOS ---
    # Filtra el DataFrame original: mantiene solo filas con 'monthly_income' menor a 1500
    monthly_income_outliers = df[(df['monthly_income'] < 1500)]

    # --- SALIDA DE RESULTADOS ---
    print("\n---- Registros Fuera de Rango (Monthly Income) ----")
    # Cuenta cuántos empleados cumplen con el criterio de bajo ingreso
    print(f"Total registros con tarifa atípica: {len(monthly_income_outliers)}")
    # Muestra en pantalla solo el número de empleado y su sueldo atípico
    print(f"\n{monthly_income_outliers[['employee_number', 'monthly_income']]}")
    print("\n")

# 4. Punto de entrada del script
if __name__ == "__main__":
    # Ejecuta la función principal
    data_low_income()