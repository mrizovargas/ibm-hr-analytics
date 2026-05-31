# ==============================================================================
# Título: Agregación y Cálculo de Rotación Laboral por Puesto
#
# Objetivo: Calcular el índice de deserción (attrition) de los empleados según
# su puesto.
#
# Descripción: Este script importa un conjunto de datos previamente limpio de
# Recursos Humanos,transforma la variable de deserción ("Yes"/"No") en un valor
# numérico (1/0) y realiza agrupaciones por puesto de trabajo (job_role). Calcula
# métricas clave como el total de empleados, total de bajas y la tasa de rotación.
# Finalmente, exporta este resumen a un archivo CSV con una marca de tiempo única.
#
# Archivo Python: day09_job_role_attrition_rate.py
#
# Archivo CSV: day09_job_role_attrition_rate.csv
#
# Archivo PNG: day09_job_role_attrition_rate.PNG
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import pandas as pd  # Herramienta para estructurar y analizar datos en tablas.
from pathlib import Path  # Facilita la manipulación de rutas de archivos en el disco.
import logging  # Permite registrar mensajes de seguimiento e historial del proceso.
from datetime import datetime  # Ayuda a capturar la fecha y hora actual del sistema.
import sys  # Proporciona acceso a funciones y configuraciones del entorno de Python.

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Busca la ruta absoluta de la carpeta 'src' subiendo dos niveles desde este archivo.
src_dir = str(Path(__file__).resolve().parents[1])

# Si la carpeta 'src' no está en la lista de rutas de Python, la añade al inicio.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# ==============================================
# --- BLOQUE 2.1: IMPORTACIONES PERSONALIZADAS ---
# ==============================================
# Conecta con nuestra función interna para abrir conexiones seguras a la base de datos.
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.etl_pipeline import import_dataset

# Inicializa el registro de logs para documentar el proceso del pipeline.
get_logging_pipeline()

# ===================================================
# --- BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
# ===================================================
# Sube tres niveles desde este archivo para encontrar la carpeta raíz del proyecto.
# Nota técnica: Se cambió a un objeto tipo Path para permitir el uso del operador '/' más abajo.
base_dir = Path(__file__).resolve().parents[3]

# Define la ruta exacta de la carpeta donde se guardarán los reportes finales generados.
target_results_dir = base_dir / "05_results" / "rrhh" / "day09_base_aggregations"

# ===================================================
# --- BLOQUE 4: PROCESAMIENTO Y AGREGACIÓN DE DATOS ---
# ===================================================
# Invoca la función personalizada para cargar el conjunto de datos limpio en memoria.
df = import_dataset()

# Convierte el texto 'Yes'/'No' de deserción en números 1/0 para poder sumarlos matemáticamente.
df["attrition_numeric"] = df["attrition"].apply(lambda x: 1 if x == "Yes" else 0)

resultado = (
    df.groupby("job_role")[
        "attrition_numeric"
    ]  # Agrupa los datos y selecciona la columna numérica
    .agg(["count", "sum", "mean"])  # Calcula cuántos son, su suma y su promedio
    .reset_index()  # Devuelve el resultado a un formato de tabla limpio
)


# Renombra las columnas calculadas para que tengan nombres claros, profesionales y fáciles de leer.
resultado.columns = ["job_role", "total_employees", "total_attrition", "attrition_rate"]

# ===================================================
# --- BLOQUE 5: EXPORTACIÓN DE RESULTADOS A DISCO ---
# ===================================================
# Verifica si la tabla contiene información válida y no está vacía.
if not resultado.empty:
    # Muestra en la pantalla de la terminal las primeras filas para una revisión rápida.
    logging.info("====== INICIA PROCESAMIENTO DE DATOS ======")
    print("\n 👀 Vista previa del talento de alto costo en ventas:")
    print(resultado.head().to_string(index=False))

    try:
        # Crea la carpeta de destino en la computadora si no existe todavía.
        target_results_dir.mkdir(parents=True, exist_ok=True)

        # Genera una marca de tiempo actual (AñoMesDía_HoraMinutoSegundo) para el nombre del archivo.
        time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Construye el nombre final y la ruta completa del archivo CSV.
        processed_file_name = f"day09_job_role_attrition_rate_{time_stamp}.csv"
        processed_file_path = target_results_dir / processed_file_name

        # Alerta al usuario que la escritura del archivo ha comenzado.
        print("\n")
        logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

        # Guarda los datos en el disco duro, asegurando el formato de texto universal (UTF-8).
        resultado.to_csv(processed_file_path, index=False, encoding="utf-8")

        # Confirma que el archivo se guardó correctamente mostrando su ubicación.
        logging.info(f"💾 Resultado exportado con éxito en: {target_results_dir}")
        logging.info(f"📄 CSV: {processed_file_name}")
        print("\n")

    except Exception as e_export:
        # Captura y muestra cualquier error que ocurra durante la escritura del archivo.
        logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
        print("\n")
else:
    # Informa en caso de que la consulta no haya devuelto ningún resultado.
    logging.info("✨ No se encontraron registros que exportar.")
