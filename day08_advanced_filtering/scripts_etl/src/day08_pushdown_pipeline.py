# ==============================================================================
# Título: Extracción Optimizada de Datos de RRHH con Pushdown Optimization
#
# Objetivo: Extraer información financiera del personal de ventas desde
# PostgreSQL.
#
# Descripción: El script conecta a una base de datos, filtra los datos pesados
# directamente en el motor relacional (Pushdown) para no saturar la red, y
# guarda el resultado en un archivo CSV.
#
# Archivo Python: day08_pushdown_pipeline.py
#
# Archivo CSV: day08_pushdown_pipeline.csv
#
# Archivo PNG: day08_pushdown_pipeline.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import pandas as pd  # Para manipular y estructurar los datos en tablas.
import time  # Para medir el rendimiento y tiempos de ejecución.
from pathlib import (
    Path,
)  # Para gestionar rutas de archivos de forma compatible con cualquier S.O.
import logging  # Para mostrar mensajes de estado organizados en la consola.
import sys  # Para interactuar con el sistema operativo y el entorno de Python.
from datetime import datetime  # Para registrar fechas y horas exactas.

# Configura las alertas de la consola para que muestren la hora, el tipo de mensaje y el texto.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

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
from custom_functions.security_engine import get_secure_engine

# ===================================================
# --- BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
# ===================================================
# Sube tres niveles desde este archivo para encontrar la carpeta raíz del proyecto.
base_dir = Path(__file__).resolve().parents[3]

# Define la ruta exacta donde se guardarán los resultados procesados de recursos humanos.
target_results_dir = base_dir / "05_results" / "rrhh" / "day08_advanced_filtering"


# ==================================================================
# --- BLOQUE 4: FUNCIÓN PRINCIPAL DE EXTRACCIÓN Y OPTIMIZACIÓN ---
# ==================================================================
def ejecutar_extraccion_pushdown():
    """Ejecuta la conexión, aplica el filtro en la base de datos y exporta el resultado."""

    # Anuncia en la consola que se está iniciando el proceso de conexión.
    print("\n")
    logging.info("====== 🗄️ INICIANDO CONEXIÓN A PostgreSQL ======")
    logging.info("⏳ Conectando al motor relacional de PostgreSQL...")

    # Activa el motor de conexión segura.
    engine = get_secure_engine()

    # Anuncia el inicio de la estrategia de optimización de datos.
    logging.info("====== 🎯 IMPLEMENTACIÓN DE PUSHDOWN OPTIMIZATION ======")

    # Define la consulta SQL para filtrar los datos pesados directamente en el servidor.
    query_gobernada = """
        SELECT employee_number, department, job_role, monthly_income 
        FROM employee_master_data 
        WHERE department = 'Sales' AND monthly_income > 10000;
    """

    # Toma el tiempo exacto antes de iniciar la descarga por red.
    start_time = time.time()

    # Envía la consulta a la base de datos y recibe el resultado ya filtrado en un DataFrame.
    df_radar_ventas = pd.read_sql(query_gobernada, con=engine)

    # Toma el tiempo exacto al terminar la descarga de datos.
    end_time = time.time()

    # Reporta el éxito de la operación y las métricas de rendimiento en la consola.
    logging.info("✅ Datos recibidos en memoria mediante Pushdown exitoso.")
    logging.info(
        f"⏱️ Tiempo total de transferencia por red: {round(end_time - start_time, 4)} segundos."
    )
    logging.info(
        f"📊 Cantidad de filas que viajaron por la red: {len(df_radar_ventas)}"
    )

    # Muestra en la pantalla de la terminal las primeras filas para una revisión rápida.
    print("\n👀 Vista previa del talento de alto costo en ventas:")
    print(df_radar_ventas.head().to_string(index=False))

    # ==================================================================
    # --- BLOQUE 5: EXPORTACIÓN DE RESULTADOS A DISCO ---
    # ==================================================================
    # Verifica si la tabla contiene información válida y no está vacía.
    if not df_radar_ventas.empty:
        try:
            # Crea la carpeta de destino en la computadora si no existe todavía.
            target_results_dir.mkdir(parents=True, exist_ok=True)

            # Genera una marca de tiempo actual (AñoMesDía_HoraMinutoSegundo) para el nombre del archivo.
            time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Construye el nombre final y la ruta completa del archivo CSV.
            processed_file_name = f"day08_pushdown_extraction_{time_stamp}.csv"
            processed_file_path = target_results_dir / processed_file_name

            # Alerta al usuario que la escritura del archivo ha comenzado.
            print("\n")
            logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

            # Guarda los datos en el disco duro, asegurando el formato de texto universal (UTF-8).
            df_radar_ventas.to_csv(processed_file_path, index=False, encoding="utf-8")

            # Confirma que el archivo se guardó correctamente mostrando su ubicación.
            logging.info(f"💾 Resultado exportado con éxito en: {target_results_dir}")
            logging.info(f"📄 CSV: {processed_file_name}")

        except Exception as e_export:
            # Captura y muestra cualquier error que ocurra durante la escritura del archivo.
            logging.info(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")

        print("\n")
    else:
        # Informa en caso de que la consulta no haya devuelto ningún registro de ventas.
        logging.info(
            "✨ No se encontraron registros que cumplan con las condiciones. Nada que exportar."
        )


# ==================================
# --- BLOQUE 6: PUNTO DE ENTRADA ---
# ==================================
# Asegura que el script solo corra si se ejecuta directamente, y no al ser importado por otro código.
if __name__ == "__main__":
    ejecutar_extraccion_pushdown()
