# ==============================================================================
# Título: Pipeline de Imputación Inteligente de Satisfacción Laboral
#
# Objetivo: Rellenar los valores nulos en la satisfacción laboral usando la
# mediana de cada departamento.
#
# Descripción: Este script prepara el entorno del proyecto, carga un conjunto de
# datos brutos y resuelve el problema de los datos faltantes en la columna
# 'job_satisfaction'. En lugar de usar un promedio general que sesgaría los datos,
# calcula la mediana específica de cada departamento para rellenar los huecos de
# forma más realista. Al final, verifica que la limpieza haya sido exitosa.
#
# Archivo Python: day11_impute_job_satisfaction.py
#
# Archivo PNG: day11_impute_job_satisfaction.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
# Importamos herramientas estándar para manejo de datos, sistema y registros (logs).
import pandas as pd  # Herramienta principal para la manipulación y análisis de datos
import sys  # Permite interactuar con el sistema (usado para configurar rutas)
import logging  # Utilidad para registrar mensajes de estado o errores del programa
from pathlib import Path  # Facilita la manipulación de rutas de archivos y carpetas

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Obtiene la ruta del directorio principal del proyecto (dos niveles arriba del archivo actual)
src_dir = str(Path(__file__).resolve().parents[1])

# Si esa ruta raíz no está registrada en el sistema de Python, la agregamos al inicio.
if not src_dir in sys.path:
    sys.path.insert(0, src_dir)

# =============================================
# --- BLOQUE 3: CARGA Y REGISTRO DE EVENTOS ---
# =============================================
# Importamos funciones personalizadas creadas específicamente para este proyecto.
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.etl_dirty_pipeline import import_dataset

# Activamos el sistema de alertas/logs para registrar el progreso en la consola.
get_logging_pipeline()


# ================================
# --- BLOQUE 4: CARGA DE DATOS ---
# ================================
# Traemos la información en bruto invocando nuestra función personalizada y la guardamos en un DataFrame (df).
df = import_dataset()


# ============================================================
# --- BLOQUE 5: ESTRATEGIA DE MANEJO DE NULOS (IMPUTACIÓN) ---
# ============================================================
# Calculamos la mediana de satisfacción para cada departamento y la expandimos
# para que coincida con el tamaño original del archivo (así se puede emparejar fila por fila).
medianas_por_dept = df.groupby("department")["job_satisfaction"].transform("median")

# Revisamos la columna de satisfacción: los valores vacíos (NaN) se reemplazan con la mediana de su
# respectivo departamento.
df["job_satisfaction"] = df["job_satisfaction"].fillna(medianas_por_dept)


# ===================================================
# --- BLOQUE 6: VERIFICACIÓN Y CONTROL DE CALIDAD ---
# ===================================================
# Contamos cuántos valores nulos quedaron en la columna para asegurarnos de que el proceso funcionó.
nulos_restantes = df["job_satisfaction"].isnull().sum()

# Mostramos en pantalla el conteo de nulos (lo ideal es que sea 0).
print(f"Valores nulos en job_satisfaction: {nulos_restantes}")

# Imprimimos las primeras 5 filas de las columnas involucradas para auditar visualmente el resultado.
print(df[["department", "job_satisfaction"]].head())
print("\n")
