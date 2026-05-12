# ----------------------------------------------------------------------------
# Título: Extractor y Analizador de Tipos de Datos (Maestra de Empleados)
# 
# Objetivo: Conectarse a una base de datos PostgreSQL, leer la tabla maestra 
# de empleados y mostrar los tipos de datos de cada columna para asegurar la 
# integridad de la información.
# 
# Descripción: El script utiliza variables de entorno para una conexión segura, 
# ejecuta una consulta SQL para traer los datos a un DataFrame de Pandas y 
# finalmente imprime en consola cómo ha interpretado Pandas cada columna (fechas, 
# enteros, textos, etc.).
# 
# Archivo Python: day04_empl_mstr_data_types.py
# 
# Archivo PNG: day04_empl_mstr_data_types.png
# ----------------------------------------------------------------------------

import pandas as pd  # Biblioteca para manipulación y análisis de datos
from sqlalchemy import create_engine  # Motor para gestionar la conexión SQL
import os  # Biblioteca para leer variables del sistema operativo
from dotenv import load_dotenv  # Para cargar credenciales seguras desde un archivo .env

# 1. Configuración del entorno
load_dotenv()  # Carga las credenciales (usuario, pass, host) del archivo .env

# 2. Conexión a la base de datos
# Se construye la cadena de conexión usando las variables de entorno
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# 3. Definición de la consulta
# Query SQL para extraer toda la información de la tabla de empleados
query = """
SELECT * FROM employee_master_data
"""

# 4. Definición de la función lógica
def empl_mstr_data_types():
    """
    Función que lee los datos de SQL y muestra sus tipos.
    """
    # Ejecuta la consulta y carga los datos en un DataFrame (estructura de tabla de Pandas)
    df = pd.read_sql(query, con = engine)
    
    # Imprime encabezado y los tipos de datos (.dtypes) de cada columna
    print("\n---- Tipos de Datos (Tabla Maestra) ----")
    print(df.dtypes)
    print("\n")

# 5. Ejecución del script
if __name__ == "__main__":
    # Llama a la función principal si el script se ejecuta directamente
    empl_mstr_data_types()