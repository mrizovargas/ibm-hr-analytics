# ------------------------------------------------------------------------------------
# Título: Detección de Valores Atípicos en Recursos Humanos
# 
# Objetivo: Identificar empleados con ingresos mensuales inusualmente bajos.
# 
# Descripción: Este script carga un dataset de RRHH, estandariza los nombres de las
# columnas a 'snake_case' y filtra registros donde el 'monthly_income' es menor a 1500,
# para detectar posibles errores de entrada de datos o casos especiales.
# 
# Archivo Pyhton: day04_analyze_data_low_income_01.py
# 
# Archivo PNG: day04_analyze_data_low_income_01.png
# ------------------------------------------------------------------------------------

# Librería para manipulación y análisis de datos
import pandas as pd
# Módulo para leer/escribir archivos CSV
import csv
# Módulo para interactuar con el sistema operativo (rutas de archivos)
import os
# Módulo para manejo moderno y multiplataforma de rutas
from pathlib import Path
# Módulo para expresiones regulares (búsqueda de patrones de texto)
import re

# --- Configuración de Rutas ---
# Define la carpeta raíz del proyecto subiendo 3 niveles desde donde está este script
base_dir = Path(__file__).resolve().parents[3]

# Construye la ruta exacta hacia la carpeta de datos crudos de rrhh
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'

# Define el nombre del archivo y construye la ruta completa
rrhh_file_name = 'IBM_HR_Dirty_Practices'
rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")


# --- Funciones ---
def to_snake_case(name):
    """
    Convierte textos de CamelCase o PascalCase a snake_case (ej: 'MonthlyIncome' -> 'monthly_income').
    Mejora la legibilidad y estándar de las columnas.
    """
    # Inserta guion bajo antes de letras mayúsculas seguidas de minúsculas
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Convierte a minúsculas y separa con guion bajo
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# --- Proceso Principal ---
try:
    # Intenta leer el archivo CSV y cargarlo en un DataFrame de pandas
    df = pd.read_csv(rrhh_path_csv)
    
    # Aplica la función para estandarizar todos los nombres de columnas a snake_case
    # Nota: Se corrigió 'df.colums' a 'df.columns' para evitar error
    df.columns = [to_snake_case(col) for col in df.columns]
    
except Exception as e:
    # Si hay error (archivo no existe, error de lectura), avisa y deja el df como None
    print(f"❌ Error al cargar o procesar el dataset: {e}")
    df = None


# --- Análisis de Datos ---
if df is not None:
    # Filtra el DataFrame buscando empleados con un ingreso menor a 1500
    monthly_income_outliers = df[(df['monthly_income'] < 1500)]
    
    # Imprime los resultados obtenidos
    print("\n---- Registros Fuera de Rango (Monthly Income) ----")
    print(f"Total registros con tarifa atípica: {len(monthly_income_outliers)}")
    print(f"\n{monthly_income_outliers[['employee_number', 'monthly_income']]}")
    print("\n")