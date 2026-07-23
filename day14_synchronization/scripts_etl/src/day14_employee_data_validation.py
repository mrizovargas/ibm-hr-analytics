# =====================================================================
# Título: Validación y Diagnóstico Inicial del Dataset de Empleados
#
# Objetivo: Conectar, cargar y perfilar la estructura del dataset.
#
# Descripción: Este script actúa como la primera fase de un pipeline.
# Su meta es verificar que los datos de recursos humanos se carguen
# correctamente, evaluar si el archivo contiene registros y revisar
# los tipos de datos de las columnas clave (como ingresos y rotación)
# antes de dar paso a transformaciones más complejas.
#
# Archivo Python: day14_employee_data_validation.py
#
# Archivo PNG: day14_employee_data_validation.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para el programa.
# =====================================================================

# Pandas nos ayuda a manipular las tablas de datos de forma sencilla.
import pandas as pd

# Sys nos permite interactuar directamente con el sistema operativo.
import sys

# Logging nos sirve para registrar qué hace el programa paso a paso.
import logging

# Path nos ayuda a gestionar rutas de archivos sin importar el sistema.
from pathlib import Path

# =====================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que el programa sepa dónde buscar carpetas.
# =====================================================================

# Localizamos la carpeta principal del proyecto subiendo dos niveles.
src_dir = str(Path(__file__).resolve().parents[1])

# Si esa ruta no está registrada en Python, la añadimos al inicio.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Traemos la función encargada de leer el conjunto de datos de RRHH.
from custom_functions.etl_pipeline import import_dataset

# Traemos el configurador de registros para guardar bitácoras limpias.
from custom_functions.logging_pipeline import get_logging_pipeline

# Encendemos y configuramos nuestro sistema de registro o bitácora.
get_logging_pipeline()


# =====================================================================
# BLOQUE 3: PIPELINE PRINCIPAL DE DIAGNÓSTICO
# Objetivo: Validar la existencia de datos y analizar sus columnas.
# =====================================================================
def get_pipeline():
    # Dejamos un espacio en blanco en la consola por orden visual.
    print("\n")

    # Anotamos en la bitácora que la conexión va a comenzar ahora.
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON EL DATASET ====")

    # Usamos un bloque de seguridad por si algo falla durante la carga.
    try:
        # Intentamos importar y almacenar la tabla en la variable 'df'.
        df = import_dataset()

        # Si la tabla contiene información y no llegó vacía, avanzamos.
        if not df.empty:
            # Reportamos que la inspección de los datos ha comenzado.
            logging.info("🚀 ==== INICIA PROCESAMIENTO DE DATOS ====")

            # Mostramos en pantalla el número total de filas y columnas.
            print(f"Dimensiones exactas de la tabla: {df.shape}")

            # Revisamos qué tipo de dato tiene cada columna clave.
            print(
                df[
                    ["employee_id", "employee_number", "monthly_income", "attrition"]
                ].dtypes
            )

            # Dejamos otro espacio en blanco al terminar el reporte.
            print("\n")

            # Retornamos True confirmando que todo salió de maravilla.
            return True

        # En caso de que la tabla exista pero no tenga ni una sola fila:
        else:
            # Registramos que no hay datos disponibles para trabajar.
            logging.info("✨ No se encontraron registros para procesar.")
            print("\n")

            # Retornamos False para avisar que el pipeline se detiene.
            return False

    # Si ocurre un error inesperado (archivo corrupto, falta de red, etc.)
    except Exception as e:
        # Guardamos el mensaje de error exacto para poder revisarlo.
        logging.error(f"❌ Error detectado en: {e}")

        # Avisamos al sistema que la operación falló.
        return False


# =====================================================================
# BLOQUE 4: DISPARADOR DEL PROGRAMA (PUNTO DE ENTRADA)
# Objetivo: Arrancar el script de forma segura desde la terminal.
# =====================================================================
if __name__ == "__main__":
    # Hacemos una prueba rápida de lectura. Si falla al inicio, cerramos
    # el programa inmediatamente enviando un código de error (1).
    if not get_pipeline():
        sys.exit(1)
