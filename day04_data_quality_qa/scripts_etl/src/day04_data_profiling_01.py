# -----------------------------------------------------------------------------------
# Título: Perfilamiento y Validación de Datos de RRHH (IBM Attrition)
# 
# Objetivo: Cargar un dataset de recursos humanos, estandarizar los nombres de columnas 
# a formato 'snake_case' y realizar una validación de coherencia lógica en los años de 
# experiencia de los empleados.
# 
# Descripción: Este script lee un archivo CSV, limpia los nombres de las columnas para 
# facilitar su manejo, muestra estadísticas descriptivas básicas y detecta errores lógicos 
# donde los años en la empresa superan la experiencia total.
# 
# Archivo Python: day04_data_profiling_01.py
# 
# Archivo PNG: day04_data_profiling_01.png
# -----------------------------------------------------------------------------------

# Biblioteca para manipulación de datos (DataFrames)
import pandas as pd
# Biblioteca para manejar rutas de archivos en el sistema operativo
import os
# Biblioteca para manejo de archivos CSV
import csv
# Manejo de rutas de archivos de forma compatible entre SO
from pathlib import Path
# Biblioteca para usar expresiones regulares (limpieza de texto)
import re

# --- CONFIGURACIÓN DE RUTAS ---
# Define el directorio base subiendo 3 niveles desde donde está este script
base_dir = Path(__file__).resolve().parents[3]
# Construye la ruta hacia la carpeta específica de datos crudos de rrhh
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'
# Define el nombre del archivo sin extensión
rrhh_file_name = 'IBM_HR_Dirty_Practices'

# Une el directorio y el nombre del archivo para obtener la ruta completa del CSV
rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

# --- FUNCIONES ---
def to_snake_case(name):
    """Convierte texto estilo CamelCase o PascalCase a snake_case (minúsculas y guiones bajos)."""
    # Inserta guion bajo antes de letras mayúsculas seguidas de minúsculas
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Inserta guion bajo antes de letras mayúsculas al final y convierte todo a minúsculas
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# --- PROCESAMIENTO ---
try:
    # Intenta cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(rrhh_path_csv)
    # Estandariza los nombres de las columnas a snake_case para mayor legibilidad
    df.columns = [to_snake_case(col) for col in df.columns]

    # Validación de integridad de tipos antes de la auditoría
    def safety_check(df):
        cols_to_fix = ['age', 'years_at_company', 'total_working_years']
        for col in cols_to_fix:
            # Forzar a numérico y llenar vacíos con 0 para evitar errores lógicos
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        print("\n✅ Safety Check: Tipos de datos alineados para comparación lógica.")
        return df
    
    df = safety_check(df)

except Exception as e:
    # Si hay error (archivo no encontrado, etc.), imprime el error y establece el DataFrame como None
    print(f"❌ Error al cargar o procesar el dataset: {e}")
    df = None

# --- ANÁLISIS Y VALIDACIÓN ---
if df is not None:
    # Imprime el perfilamiento estadístico de variables clave (edad, ingresos, años de trabajo)
    print("\n---- 🔍 Perfilamiento Estadístico de IBM HR ----")
    print(df[['age', 'monthly_income', 'total_working_years']].describe())

    # --- VALIDACIÓN LÓGICA ---
    # Busca empleados donde la antigüedad en la empresa supera su experiencia laboral total (error lógico)
    errors = df[df['years_at_company'] > df['total_working_years']]

    if not errors.empty:
        # Si encuentra errores, muestra la alerta y los registros afectados
        print(f"\n⚠️ ¡ALERTA! Se encontraron {len(errors)} empleados con más años en la empresa que años trabajados en total.")
        print(errors[['employee_number', 'years_at_company', 'total_working_years']])
    else:
        # Si no hay errores, confirma que la validación fue exitosa
        print("\n✅ Coherencia temporal: Validada.")
        print("\n")