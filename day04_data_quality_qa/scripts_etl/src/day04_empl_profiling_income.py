# ---------------------------------------------------------------------------------
# Título: Análisis Exploratorio de Salarios (Profiling)
# 
# Objetivo: Analizar la distribución de los salarios mensuales de los empleados.
# 
# Descripción: El script conecta a una base de datos PostgreSQL, extrae los datos de
# empleados, calcula estadísticas descriptivas del salario mensual e identifica
# valores atípicos (outliers) que sesgan la media, permitiendo entender la estructura
# salarial real.
# 
# Archivo Python: day04_empl_profiling_income.py
# 
# Archivo PNG: day04_empl_profiling_income.png
# ---------------------------------------------------------------------------------

# --- IMPORTACIÓN DE LIBRERÍAS ---
# 'pandas' Biblioteca para manipulación de datos
import pandas as pd
# 'create_engine' Herramienta para crear la conexión a la base de datos
from sqlalchemy import create_engine
# 'os' Biblioteca para leer variables de entorno
import os
# 'load_env' Herramienta para cargar las credenciales desde un archivo .env
from dotenv import load_dotenv

# Carga las variables de entorno (credenciales) del archivo .env
load_dotenv()

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Configura la conexión a PostgreSQL usando las credenciales seguras
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Define la consulta SQL para extraer los datos maestros de empleados
query = """ 
SELECT * FROM employee_master_data 
"""

# --- FUNCIÓN PRINCIPAL DE ANÁLISIS ---
def profiling_analysis():
    """
    Función principal para ejecutar el análisis de perfilado de salarios.
    """
    # 1. Extracción de datos: Lee la consulta SQL y la carga en un DataFrame de pandas
    df = pd.read_sql(query, con = engine)
    
    # 2. Selección de variable: Filtra solo la columna de salario mensual
    income = df['monthly_income']
    
    # 3. Cálculo de estadísticas descriptivas
    mean_income = income.mean()      # Promedio
    median_income = income.median()  # Valor central (mediana)
    std_income = income.std()        # Dispersión (desviación estándar)
    min_income = income.min()        # Salario más bajo
    max_income = income.max()        # Salario más alto
    
    # 4. Visualización de estadísticas generales
    print("\n---- Análisis de Salarios Mensuales (monthly_income) ----")
    print(f"Promedio (Media): {mean_income:,.2f}")
    print(f"Mediana: {median_income:,.2f}")
    print(f"Desviación Estándar: {std_income:,.2f}")
    print(f"Mínimo: {min_income:,.2f}")
    print(f"Máximo: {max_income:,.2f}")
    print("-" * 50)
    
    # 5. Detección de Outliers (Valores atípicos)
    # Define el límite superior: Media + 3 veces la desviación estándar
    threshold = mean_income + (3 * std_income)
    # Filtra los empleados que ganan más del límite
    outliers = df[df['monthly_income'] > threshold]
    
    # 6. Muestra resultados del análisis de outliers
    print(f"\n[Pitfall] La media de ${mean_income:,.2f} está inflada por outliers (valores atípicos).")
    print(f"Empleados con salario > 3 desviaciones estándar ({len(outliers)} empleados).")
    # Muestra los 5 salarios más altos atípicos
    print(outliers[['job_role', 'monthly_income', 'job_level']].sort_values(by = 'monthly_income', ascending = False).head(5))
    
    # 7. Conclusión del análisis
    print("\n[Conclusión] Al contrastar con la mediana:")
    print(f"El 50% de los empleados gana menos de ${median_income:,.2f},")
    print(f"mientras que el promedio es de ${mean_income:,.2f}.")
    print("la diferencia muestra una distribución sesgada a la derecha (pocos ganan mucho).")
    print("\n")

# --- PUNTO DE ENTRADA ---
# Punto de entrada principal del script
if __name__ == "__main__":
    profiling_analysis()