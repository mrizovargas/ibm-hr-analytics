# ==============================================================================
# Título: Procesamiento Inicial de Datos de Riesgo RRHH
# 
# Objetivo: Cargar y validar la estructura del archivo CSV de empleados.
# 
# Descripción: Este script localiza un archivo específico de recursos humanos
# (riesgo de fuga), lo lee usando pandas y muestra un resumen técnico (info) y 
# las primeras filas para asegurar que los datos se han cargado correctamente.
#
# Resultado PNG: day02_empl_risk_data_cleaning.png
# ==============================================================================

import pandas as pd  # Biblioteca para manipular y analizar los datos
import os            # Biblioteca para gestionar rutas de archivos en el sistema operativo
from pathlib import Path # Biblioteca moderna para gestionar rutas de archivos de forma independiente al SO

# ---------------------------------------------------------
# 1. Configuración de rutas.
# ---------------------------------------------------------

# Localizamos la carpeta raíz del proyecto subiendo 3 niveles desde este archivo.
base_dir = Path(__file__).resolve().parents[3]

# Construye la ruta hacia la carpeta específica de datos procesados de RRHH.
target_raw_dir = base_dir / '02_data' / 'processed' / 'rrhh'

# Crea la ruta final apuntando directamente al archivo CSV que necesitamos.
rrhh_path_csv = target_raw_dir / 'employees_attrition.csv'


# ---------------------------------------------------------
# 2. Carga y visualización de datos.
# ---------------------------------------------------------

# Comprueba si el archivo físico existe en la ruta indicada para evitar errores de lectura.
if rrhh_path_csv.exists():
    # Carga el contenido del CSV en una tabla de datos (DataFrame).
    df = pd.read_csv(rrhh_path_csv)
    # Informa al usuario que la carga fue exitosa y muestra cuántas filas tiene originalmente.
    print(f"✅ Archivo cargado con éxito. Filas iniciales: {len(df)}")
else:
    # Si el archivo no está, detiene el programa y lanza un mensaje de error claro.
    raise FileNotFoundError(f"❌ No se encontró el archivo en: {rrhh_path_csv}")

# Imprime un resumen técnico de la tabla (nombres de columnas y tipos de datos).
print("\nResumen técnico (datos crudos):")
print(df.info())

# Muestra las primeras 5 filas para una revisión visual rápida de la información.
print("\nVista previa (datos crudos):")
print(df.head())


# ---------------------------------------------------------
# 3. Eliminación de duplicados
# ---------------------------------------------------------

# Identifica y borra filas repetidas basándose solo en el número de empleado.
# .copy() asegura que trabajamos sobre una tabla nueva e independiente.
df_clean = df.drop_duplicates(subset="employee_number").copy()

# Imprime el total de registros restantes para confirmar cuántos duplicados se borraron.
print(f"Registros tras eliminar duplicados: {df_clean.shape[0]}")


# ---------------------------------------------------------
# 4. Transformación de tipos de datos
# ---------------------------------------------------------

# Definimos un diccionario que asocia la columna con el tipo de dato deseado (entero).
cols_to_fix = {
    "monthly_income": int,
    "job_satisfaction": int
}

try:
    # Intenta aplicar el cambio de formato a las columnas del diccionario de una sola vez.
    df_clean = df_clean.astype(cols_to_fix)
    print("\nTransformación de tipos completada con éxito.")
except KeyError as e:
    # Si alguna columna del diccionario no existe en la tabla, nos avisa cuál falta.
    print(f"Error: No se encontró la columna {e}")


# ---------------------------------------------------------
# 5. Validación final del proceso
# ---------------------------------------------------------

# Muestra el resumen técnico final para confirmar que los cambios de tipo se aplicaron.
print("\nResumen técnico final:")
print(df_clean.info())

# Muestra una vista previa de la tabla ya limpia y transformada.
print("\nVista previa de datos limpios:")
print(df_clean.head())