#------------------------------------------------------------------------------------
# Título: Análisis de Antigüedad Laboral
# 
# Objetivo: Extraer datos de empleados desde una base de datos PostgreSQL y generar 
# un reporte estadístico básico sobre la antigüedad (años en la empresa).
# 
# Descripción: El script se conecta a la base de datos, extrae la información, calcula 
# métricas estadísticas de la columna 'years_at_company', detecta valores nulos y 
# audita registros con edades inconsistentes (>100 años).
#
# Archivo Python: day04_empl_tenure_analysis.py
# 
# Archivo PNG: day04_empl_tenure_analysis.png
# ------------------------------------------------------------------------------------

# ==========================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ==========================================
# 'pandas': Biblioteca para manipular y analizar datos.
import pandas as pd
# 'create_engine': Herramienta para conectar con la base de datos.
from sqlalchemy import create_engine
# 'os': Biblioteca para manejar rutas y variables de entorno.
import os
# 'load_dotenv': Herramienta para cargar credenciales secretas desde un archivo .env
from dotenv import load_dotenv

# ==========================================
# 2. CONFIGURACIÓN Y CONEXIÓN
# ==========================================
# Carga las variables de seguridad del archivo .env (usuario, pass, host, etc.)
load_dotenv()

# Crea la conexión a la base de datos PostgreSQL usando los datos seguros
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Definimos la consulta SQL para traer la información completa
query = """ 
SELECT * FROM employee_master_data 
"""

# ==========================================
# 3. FUNCIONES DE ANÁLISIS
# ==========================================
def empl_tenure_analysis():
    """
    Función principal: Extrae datos, genera métricas estadísticas,
    revisa nulos y audita edades incoherentes.
    """
    
    # Ejecuta la consulta y carga los datos en un DataFrame de pandas
    df = pd.read_sql(query, con=engine) # Corrección: pd.read_sql, no create_engine
    
    # --- A. Perfil Estadístico ---
    # Calcula métricas (media, desviación, min, max, cuartiles) de la columna 'years_at_company'
    stadistic_profile = df['years_at_company'].describe()
    print("---- Perfil Estadístico de Antigüedad ----")
    print(stadistic_profile)
    
    # --- B. Auditoría de Valores Nulos ---
    # Cuenta cuántos campos vacíos hay por columna
    nulls_values = df.isnull().sum()
    print("\n---- Valores Nulos por Columna ----")
    print(nulls_values)
    
    # --- C. Auditoría de Edad ---
    # Filtra y muestra empleados con edad mayor a 100 (datos erróneos)
    age_audit = df[df['age'] > 100]
    print("\n---- Auditoría de Edad (Mayores de 100 años) ----")
    print(age_audit)
    print("\n")

# ==========================================
# 4. EJECUCIÓN DEL SCRIPT
# ==========================================
if __name__ == "__main__":
    # Inicia la función de análisis
    empl_tenure_analysis()