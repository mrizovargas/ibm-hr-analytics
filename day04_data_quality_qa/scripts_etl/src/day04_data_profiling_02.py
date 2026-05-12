# ------------------------------------------------------------------------------
# Título: Análisis de Calidad de Datos - IBM HR
# 
# Objetivo: Realizar un perfilamiento estadístico y validar la coherencia lógica 
# de los datos de empleados (años en la empresa vs años totales).
# 
# Descripción: Este script extrae datos de una base de datos PostgreSQL, calcula 
# estadísticas básicas (media, máximo, etc.) de campos clave y busca incongruencias 
# en la experiencia laboral de los empleados.
# 
# Achivo Python: day04_data_profiling_02.py
# 
# Archivo PNG: day04_data_profiling_02.png
# -------------------------------------------------------------------------------

# Biblioteca para manipulación y análisis de datos
import pandas as pd
# Módulo para conectar con la base de datos
from sqlalchemy import create_engine
# Módulo para leer variables de entorno del sistema
import os
# Carga variables desde un archivo .env
from dotenv import load_dotenv

# 1. Configuración del entorno y conexión
# Carga las variables de entorno (credenciales) desde un archivo .env oculto
load_dotenv()

# Crea la conexión a la base de datos PostgreSQL usando credenciales seguras
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# 2. Definición de la consulta SQL
# Define la consulta SQL para extraer toda la información de la tabla de empleados
query = """
    SELECT *
    FROM
        employee_master_dirty_data
"""

# 3. Función principal de perfilamiento
def data_profiling():
    """Realiza la extracción, análisis estadístico y validación de reglas."""
    
    # Lee la tabla SQL y la carga en un DataFrame de Pandas
    df = pd.read_sql(query, con = engine)

    # Validación de integridad de tipos antes de la auditoría
    def safety_check(df):
        cols_to_fix = ['age', 'years_at_company', 'total_working_years']
        for col in cols_to_fix:
            # Forzar a numérico y llenar vacíos con 0 para evitar errores lógicos
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        print("\n✅ Safety Check: Tipos de datos alineados para comparación lógica.")
        return df
    
    df = safety_check(df)

    # Imprime estadísticas descriptivas de columnas clave: edad, ingresos y antigüedad
    print("\n---- 🔍 Perfilamiento Estadístico de IBM HR ----")
    print(df[['age', 'monthly_income', 'years_at_company']].describe())

    # --- Validación de Reglas de Negocio ---
    # Busca empleados cuya antigüedad en la empresa sea mayor que el total de años trabajados (ilógico)
    errors = df[df['years_at_company'] > df['total_working_years']]

    # Verifica si se encontraron errores
    if not errors.empty:
        # Reporta el número de errores encontrados
        print(f"\n⚠️ ¡Alerta! Se encontraron {len(errors)} empleados con más años en la empresa que años trabajados en total.")
        # Muestra los detalles de los empleados con errores
        print(errors[['employee_number', 'years_at_company', 'total_working_years']])
    else:
        # Informa que no se encontraron incongruencias
        print("\n✅ Coherencia temporal: Validada.")

# 4. Ejecución del script
if __name__ == "__main__":
    # Llama a la función principal
    data_profiling()