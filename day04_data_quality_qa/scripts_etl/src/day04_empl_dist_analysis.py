# ------------------------------------------------------------------------------
# Título: Script de Análisis Exploratorio de Empleados
# 
# Objetivo: Generar un reporte rápido del conteo de registros en variables clave.
# 
# Descripción: Este script se conecta a una base de datos PostgreSQL, extrae 
# información de empleados y calcula la distribución de valores en columnas 
# específicas (rotación, departamento, rol y satisfacción) para entender la 
# composición del personal.
# 
# Archivo Python: day04_empl_dist_analysis.py
# 
# Archivo PNG: day04_empl_dist_analysis.png
# ------------------------------------------------------------------------------

# ==========================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ==========================================
import pandas as pd  # Para manejo y análisis de datos
from sqlalchemy import create_engine  # Para gestionar la conexión a la BD
import os  # Para interactuar con el sistema operativo
from dotenv import load_dotenv  # Para cargar credenciales seguras (archivo .env)

# Carga las variables de entorno (credenciales) desde el archivo .env
load_dotenv()

# ==========================================
# 2. CONFIGURACIÓN DE CONEXIÓN
# ==========================================
# Crea el motor de conexión utilizando las credenciales ocultas
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ==========================================
# 3. DEFINICIÓN DE LA FUNCIÓN DE ANÁLISIS
# ==========================================
def empl_dist_analysis():
    """
    Función que ejecuta una consulta, obtiene los datos y muestra 
    el conteo de valores en consola.
    """

    # Consulta SQL para traer toda la tabla de empleados
    query = """
        SELECT *
        FROM
            employee_master_data
    """

    # Lee la consulta SQL y la almacena en un DataFrame de pandas
    df = pd.read_sql(query, con = engine)

    # Imprime resultados del análisis
    print("---- Reporte de Conteo por Columna ----")
    
    # Muestra cuántos empleados están activos vs rotados
    print("\n---- Empleados Activos vs Rotados ----")
    print(df['attrition'].value_counts())
    
    # Muestra el porcentaje (%) de empleados por departamento
    print("\n---- % Empleados por Departamento ----")
    print(df['department'].value_counts(normalize = True) * 100)
    
    # Muestra los roles de trabajo ordenados de menor a mayor frecuencia
    print("\n---- Empleados por Roles de Trabajo Ordenados de Menor a Mayor Frecuencia ----")
    print(df['job_role'].value_counts(ascending = True))
    
    # Muestra niveles de satisfacción, incluyendo si hay valores nulos (NaN)
    print("\n---- Distibución de Empleados por Nivel de Satisfacción ----")
    print(df['job_satisfaction'].value_counts(dropna = False))
    
    print("----------------------------------------")

# ==========================================
# 4. EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    # Llama a la función si el script se ejecuta directamente
    empl_dist_analysis()