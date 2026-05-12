# -------------------------------------------------------------------------------------
# Título: Limpieza y Análisis Inicial de Datos de RRHH
# 
# Objetivo: Cargar un dataset de rotación de personal (HR Attrition) y estandarizar los 
# nombres de las columnas a formato 'snake_case' para facilitar su manejo.
# 
# Descripción: El script localiza un archivo CSV específico en el proyecto, carga los 
# datos, aplica una transformación a los nombres de las columnas para que sean más legibles 
# (ej: "NombreColumna" -> "nombre_columna") y muestra un reporte de valores nulos.
# 
# Archivo Python: day04_empl_null_validation_01.py
# 
# Archivo PNG: day04_empl_null_validation_01.png
# -------------------------------------------------------------------------------------

# Importa la librería para manipulación de datos (DataFrames)
import pandas as pd
# Importa el módulo para trabajar con archivos CSV
import csv
# Importa funciones para interactuar con el sistema operativo
import os
# Importa Path para manejo de rutas de archivos más limpio
from pathlib import Path
# Importa el módulo de expresiones regulares para manipulación de texto
import re

# --- Configuración de Rutas ---
# Define la ruta base buscando 3 niveles arriba del archivo actual (para encontrar la raíz del proyecto)
base_dir = Path(__file__).resolve().parents[3]
# Define la carpeta donde se encuentra el archivo "raw" (crudo) de recursos humanos
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'
# Define el nombre del archivo sin extensión
rrhh_file_name = 'IBM_HR_Dirty_Practices'
# Une la ruta de la carpeta y el nombre del archivo para obtener la ruta completa del CSV
rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

# --- Función para estandarizar nombres ---
def to_snake_case(name):
    """Convierte cadenas CamelCase o PascalCase a snake_case (minúsculas y guiones bajos)."""
    # Inserta guion bajo entre minúsculas y mayúsculas
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Convierte a minúsculas y separa con guion bajo las mayúsculas restantes
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# --- Bloque Principal: Carga y Procesamiento ---
try:
    # Intenta cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(rrhh_path_csv)
    # Renombra las columnas aplicando la función snake_case a cada una
    df.columns = [to_snake_case(col) for col in df.columns]
    print("\n✅ Datos cargados y columnas estandarizadas correctamente.")

except Exception as e:
    # Si ocurre un error (archivo no encontrado, formato inválido), muestra el error
    print(f"❌ Error al cargar o procesar el dataset: {e}")
    # Inicializa el DataFrame como None para indicar que no se cargaron datos
    df = None

# --- Reporte de Calidad de Datos ---
# Si la carga fue exitosa, muestra información útil
if df is not None:
    print("\n--- Reporte de Valores Nulos por Columna ---")
    # Calcula y muestra la suma de valores nulos (vacíos) por columna
    # Nota: Se debe usar df.isnull().sum() (con paréntesis)
    print(df.isnull().sum())
    print("--------------------------------------------")
    print("\n")