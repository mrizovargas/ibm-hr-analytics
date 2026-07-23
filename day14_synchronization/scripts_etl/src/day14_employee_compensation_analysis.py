"""
=======================================================================
Título: Pipeline de Clasificación y Análisis de Compensación Laboral

Objetivo: Identificar de forma eficiente qué empleados tienen salarios
por debajo del mercado según su rango o nivel de puesto.

Descripción: Este script lee los datos del personal y utiliza lógica
vectorizada (operaciones ultra rápidas en bloque) para evaluar los
ingresos mensuales. Si un empleado gana menos de lo establecido para su
nivel, lo etiqueta como "Por Debajo Mercado"; de lo contrario, se marca
como "Competitivo".

Archivo Python: day14_employee_compensation_analysis.py

Archivo PNG: day14_employee_compensation_analysis.png
=======================================================================
"""

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Traer las herramientas esenciales para el pipeline.
# =====================================================================
# NumPy nos ayuda a procesar datos en masa a máxima velocidad
import numpy as np

# Pandas es la herramienta principal para manejar tablas de datos
import pandas as pd

# Logging registra el historial de lo que pasa mientras corre el script
import logging

# Sys permite interactuar con el sistema operativo de tu PC
import sys

# Path ayuda a gestionar las rutas de carpetas de forma inteligente
from pathlib import Path

# =====================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Conectar el script con otras carpetas del proyecto.
# =====================================================================
# Buscamos la carpeta principal del proyecto subiendo un par de niveles
src_dir = str(Path(__file__).resolve().parents[1])

# Si el sistema no conoce esa carpeta, la agregamos a su lista de rutas
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Traemos funciones personalizadas para cargar datos y activar alertas
from custom_functions.etl_pipeline import import_dataset
from custom_functions.logging_pipeline import get_logging_pipeline

# Encendemos el sistema de bitácora para registrar eventos
get_logging_pipeline()


# =====================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# Objetivo: Aplicar las reglas de negocio sobre el sueldo de empleados.
# =====================================================================
def vectorized_logic():
    """Ejecuta el pipeline de negocio con lógica de alta velocidad."""
    print("\n")
    logging.info("==== INICIANDO LECTURA DEL DATASET ====")

    try:
        # Intentamos cargar la base de datos de los empleados
        df = import_dataset()

        # Si la tabla tiene información, procedemos con las reglas
        if not df.empty:
            logging.info("==== INICIAMOS LÓGICA VECTORIZADA ====")

            # Definimos las reglas de alerta salarial por nivel de puesto
            condiciones_salariales = [
                # Regla 1: Nivel 1 que gane menos de $2800 dólares
                (df["job_level"] == 1) & (df["monthly_income"] < 2800),
                # Regla 2: Nivel 2 que gane menos de $5500 dólares
                (df["job_level"] == 2) & (df["monthly_income"] < 5500),
            ]

            # Estas son las etiquetas asignadas si se cumple alguna regla
            opciones_estatus = ["N1_Por_Debajo_Mercado", "N2_Por_Debajo_Mercado"]

            # Evaluamos todas las reglas a la vez y creamos la columna final
            df["estatus_compensacion"] = np.select(
                condiciones_salariales,
                opciones_estatus,
                default="Competitivo",  # Si todo está bien, es competitivo
            )

            # Imprimimos una pequeña muestra del resultado en la consola
            print("\n👀 Vista Previa")
            columnas_vista = ["job_level", "monthly_income", "estatus_compensacion"]
            print(df[columnas_vista].head())
            print("\n")
            return True

        # Si el archivo está vacío, enviamos un aviso y terminamos
        else:
            logging.info("✨ No se encontraron registros.")
            print("\n")
            return False

    # Si algo falla en el camino, atrapamos el error para que no truene
    except Exception as e:
        print("\n")
        logging.error(f"❌ Fallo detectado en: {e}")
        return False


# =====================================================================
# BLOQUE 4: DISPARADOR DEL PROGRAMA
# Objetivo: Asegurar que el script se ejecute correctamente.
# =====================================================================
# Si este archivo se ejecuta directamente, se activa la función principal
if __name__ == "__main__":
    # Si la función devuelve un error (False), cerramos con código de fallo
    if not vectorized_logic():
        sys.exit(1)
