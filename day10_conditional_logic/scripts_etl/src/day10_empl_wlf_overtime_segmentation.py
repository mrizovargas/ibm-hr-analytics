# ==============================================================================
# Título: Pipeline de Segmentación de Balance Laboral y Horas Extras
#
# Objetivo: Clasificar a los empleados en categorías de balance entre vida y
# trabajo.
#
# Descripción: El programa extrae datos de empleados, evalúa sus condiciones de
# horas extras y balance personal para asignarles una etiqueta, y guarda este
# análisis detallado en un archivo CSV.
#
# Archivo Python: day10_empl_wlf_overtime_segmentation.py
#
# Archivo CSV: day10_empl_wlf_overtime_segmentation.csv
#
# Archivo PNG: day10_empl_wlf_overtime_segmentation.png
# ==============================================================================

# ==============================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas y utilidades necesarias para el programa.
# ==============================================================================
import pandas as pd  # Herramienta para manipulación y análisis de datos.
import logging  # Sistema para registrar eventos y mensajes del proceso.
import sys  # Funciones para interactuar con el sistema operativo.
from pathlib import Path  # Utilidad para manejar rutas de archivos de forma limpia.
from datetime import datetime  # Herramienta para obtener la fecha y hora actual.
import numpy as np  # Librería para operaciones matemáticas y lógica condicional.

# ==============================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO
# Objetivo: Asegurar que Python pueda encontrar todos los módulos del proyecto.
# ==============================================================================

# Busca la ruta de la carpeta 'src' subiendo dos niveles desde el archivo actual.
src_dir = str(Path(__file__).resolve().parents[1])

# Verifica si la carpeta 'src' está configurada; si no, la añade al inicio de
# las rutas de búsqueda para que Python reconozca nuestros scripts personalizados.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# ==============================================================================
# BLOQUE 2.1: IMPORTACIONES PERSONALIZADAS
# Objetivo: Traer las funciones específicas creadas para este proyecto.
# ==============================================================================

# Importa el sistema de bitácoras (logs) para documentar la ejecución.
from custom_functions.logging_pipeline import get_logging_pipeline

# Importa la función encargada de conectarse y descargar los datos.
from custom_functions.etl_pipeline import import_dataset

# Inicializa la bitácora para empezar a registrar el proceso.
get_logging_pipeline()

# ==============================================================================
# BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS
# Objetivo: Definir dónde se guardarán los resultados del análisis.
# ==============================================================================

# Sube tres niveles desde este archivo para localizar la carpeta principal del proyecto.
base_dir = Path(__file__).resolve().parents[3]

# Define la ruta exacta dentro del proyecto donde se guardarán los reportes procesados.
target_results_dir = base_dir / "05_results" / "rrhh" / "day10_conditional_logic"

# ==============================================================================
# BLOQUE 4: PROCESAMIENTO Y AGREGACIÓN DE DATOS
# Objetivo: Preparar y clasificar la información de los empleados.
# ==============================================================================

# Ejecuta la función personalizada para traer los datos a la memoria.
df = import_dataset()

# Establece las condiciones basadas en horas extras y balance de vida personal.
condiciones = [
    (df["over_time"] == "Yes") & (df["work_life_balance"] == 1),  # Condición 1
    (df["over_time"] == "No") & (df["work_life_balance"] == 1),  # Condición 2
    (df["over_time"] == "Yes") & (df["work_life_balance"] == 4),  # Condición 3
    (df["over_time"] == "No") & (df["work_life_balance"] >= 3),  # Condición 4
]

# Define los nombres o etiquetas que recibirán los empleados según las condiciones anteriores.
etiquetas = ["Crítico", "Alerta", "Equilibrado", "Excelente"]

# ==============================================================================
# BLOQUE 5: EXPORTACIÓN DE RESULTADOS A DISCO
# Objetivo: Guardar el análisis final en un archivo.
# ==============================================================================

# Verifica que la tabla de datos no esté vacía antes de continuar.
if not df.empty:

    # Escribe en la bitácora que el procesamiento ha comenzado.
    logging.info("====== INICIA PROCESAMIENTO DE DATOS ======")

    # Aplica las reglas: clasifica a los empleados y asigna 'Estandar' a los que no cumplan otra regla.
    df["categoria_balance_horas"] = np.select(
        condiciones, etiquetas, default="Estandar"
    )

    # Selecciona solo las columnas más importantes para el reporte.
    columnas_interes = [
        "employee_number",
        "department",
        "job_role",
        "over_time",
        "work_life_balance",
        "categoria_balance_horas",
    ]

    # Muestra en pantalla el encabezado de la tabla para una revisión rápida.
    print("\n👀 Vista previa:")
    print(df[columnas_interes].head().to_string(index=False))

    try:
        # Crea la carpeta de destino en tu computadora (y las intermedias) si aún no existen.
        target_results_dir.mkdir(parents=True, exist_ok=True)

        # Crea un sello de tiempo (AñoMesDía_HoraMinutoSegundo) para asegurar nombres de archivo únicos.
        time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Arma el nombre final y la ruta completa del archivo CSV.
        processed_file_name = f"day10_empl_wlf_overtime_segmentation_{time_stamp}.csv"
        processed_path_name = target_results_dir / processed_file_name

        # Alerta en la bitácora que comienza el proceso de guardado.
        print("\n")
        logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

        # Guarda la información en la ruta definida, sin incluir los números de fila y usando formato UTF-8.
        df[columnas_interes].to_csv(processed_path_name, index=False, encoding="utf-8")

        # Confirma que el archivo se guardó exitosamente y muestra dónde encontrarlo.
        logging.info(f"💾 Resultado exportado con éxito en: {target_results_dir}")
        logging.info(f"📄 CSV: {processed_file_name}")
        print("\n")

    except Exception as e_export:
        # Si ocurre algún problema al escribir el archivo, captura el error y lo registra.
        logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
        print("\n")

else:
    # Si la tabla de datos no contiene registros, notifica en la bitácora y no guarda nada.
    logging.info("✨ No se encontraron registros que exportar.")
    print("\n")
