# ==============================================================================
# Título: Validación de Datos Nulos en Base de Datos
# 
# Objetivo: Conectarse a una base de datos PostgreSQL, extraer la tabla de 
# empleados y mostrar un conteo de valores nulos (vacíos) por columna.
# 
# Descripción: Este script automatiza la revisión de calidad de datos para 
# identificar campos faltantes en 'employee_master_data' utilizando Pandas y 
# SQLAlchemy.
# 
# Archivo Python: day04_empl_null_validation_02.py
#
# Archivo PNG: day04_empl_null_validation_02.png
# ==============================================================================

# --- IMPORTACIÓN DE LIBRERÍAS ---
import pandas as pd             # Librería para manipulación y análisis de datos
from sqlalchemy import create_engine # Motor para conectar Python con SQL
import os                       # Para interactuar con el sistema operativo (leer variables de entorno)
from dotenv import load_dotenv  # Para cargar credenciales secretas desde un archivo .env

# --- CONFIGURACIÓN ---
# Carga las variables de entorno (usuario, pass, host, etc.) del archivo .env
load_dotenv()

# Crea la conexión a la base de datos PostgreSQL usando los datos seguros
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- FUNCIÓN PRINCIPAL ---
def empl_null_validation():
    """
    Realiza la consulta, carga los datos y cuenta los valores nulos.
    """
    
    # Define la consulta SQL para extraer todos los datos de la tabla de empleados
    query = """
        SELECT *
        FROM
            employee_master_dirty_data
    """

    # Ejecuta la consulta y carga el resultado en un DataFrame de Pandas
    df = pd.read_sql(query, con = engine)

    print("✅ Datos cargados correctamente.")

    # Imprime en consola la suma de valores nulos (NaN/None) por columna
    print("\n--- Reporte de Valores Nulos por Columna ---")
    print(df.isnull().sum())
    print("--------------------------------------------")

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    # Llama a la función si el script se ejecuta directamente
    empl_null_validation()