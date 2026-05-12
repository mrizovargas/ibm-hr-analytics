# --------------------------------------------------------------------------------
# Título: Procesamiento y Limpieza de Datos de Recursos Humanos
# 
# Objetivo: Cargar un dataset de rotación de personal (HR Attrition), estandarizar 
# los nombres de las columnas a formato 'snake_case' y detectar registros atípicos 
# (outliers) en la tarifa diaria (daily_rate).
# 
# Descripción: El script localiza un archivo CSV en el directorio del proyecto, lo 
# carga usando Pandas, renombra las columnas automáticamente para facilitar su uso 
# y analiza qué empleados tienen una tarifa diaria fuera del rango convencional 
# (100 - 1500).
# 
# Archivo Python: day04_daily_rate_outliers_01.py
# 
# Archivo PNG: day04_daily_rate_outliers_01.png
# --------------------------------------------------------------------------------

# Biblioteca para manipulación y análisis de datos
import pandas as pd
# Biblioteca para trabajar con archivos CSV
import csv
# Biblioteca para interactuar con el sistema operativo
import os
# Manejo de rutas de archivos de forma compatible entre SO
from pathlib import Path
# Biblioteca para expresiones regulares (búsqueda de patrones)
import re

# --- CONFIGURACIÓN DE RUTAS ---
# Define el directorio base del proyecto y localiza la carpeta 'raw/rrhh'
base_dir = Path(__file__).resolve().parents[3]
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'
rrhh_file_name = 'IBM_HR_Dirty_Practices'
# Construye la ruta absoluta completa al archivo CSV
rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

# --- FUNCIÓN DE LIMPIEZA ---
def to_snake_case(name):
    """Convierte cadenas de texto camelCase o PascalCase a snake_case."""
    # Añade un guion bajo antes de las mayúsculas (ej: 'camelCase' -> 'camel_Case')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Convierte a minúsculas y separa con guiones bajos (ej: 'camel_Case' -> 'camel_case')
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# --- CARGA Y PROCESAMIENTO DE DATOS ---
try:
    # Lee el archivo CSV y carga los datos en un DataFrame de Pandas
    df = pd.read_csv(rrhh_path_csv)
    
    # Aplica la función to_snake_case a cada nombre de columna para estandarizarlos
    df.columns = [to_snake_case(col) for col in df.columns]
    
except Exception as e:
    # Captura y reporta cualquier error durante la carga o procesamiento
    print(f"❌ Error al cargar o procesar el dataset: {e}")
    df = None  # Asegura que el DataFrame no tenga valores inválidos si falla

# --- ANÁLISIS DE OUTLIERS ---
# Verifica si el dataframe fue cargado correctamente antes de analizar
if df is not None:
    # Filtra empleados con 'daily_rate' inusualmente bajo (< 100) o alto (> 1500)
    outliers = df[(df['daily_rate'] < 100) | (df['daily_rate'] > 1500)]
    
    # Imprime el resultado de la detección de registros fuera de rango
    print('\n---- Registros Fuera de Rango (Daily Rate) ----')
    print(f'Total registros con tarifa atípica: {len(outliers)}')
    print("\n")