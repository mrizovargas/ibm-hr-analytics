# ==============================================================================
# Título: Pipeline de Agregación y Respaldo de Datos Financieros de RRHH
#
# Objetivo: Extraer datos de recursos humanos desde una base de datos PostgreSQL,
# validar la calidad de la información financiera y exportarla de forma segura a
# un archivo CSV con marca de tiempo.
#
# Descripción: Este script automatiza la extracción de un resumen financiero de
# RRHH. Primero, se conecta a la base de datos utilizando protocolos de seguridad
# internos. Luego, verifica que no existan anomalías en los datos (como nóminas
# con valores negativos). Finalmente, guarda una copia de seguridad local (en
# formato CSV) para su posterior análisis o auditoría, registrando cada paso
# mediante un sistema de logs.
#
# Archivo Python: day09_financial_aggregator.py
#
# Archivo CSV: day09_financial_aggregator.csv
#
# Archivo PNG: day09_financial_aggregator.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import pandas as pd  # Librería para el manejo y análisis de datos en tablas.
import logging  # Herramienta para registrar eventos y mensajes del sistema.
import sys  # Módulo para interactuar con el sistema operativo (ej. detener el script).
from pathlib import (
    Path,
)  # Utilidad para manejar rutas de carpetas y archivos de forma limpia.
import time  # Módulo para medir tiempos de ejecución (ej. duración de la conexión).
from datetime import datetime  # Permite obtener la fecha y hora actual exacta.

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Busca la ruta de la carpeta 'src' subiendo dos niveles desde la ubicación actual del archivo.
src_dir = str(Path(__file__).resolve().parents[1])

# Verifica si la carpeta 'src' ya está configurada en el sistema; si no, la añade al inicio
# para que Python pueda encontrar nuestros módulos personalizados.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# ==============================================
# --- BLOQUE 2.1: IMPORTACIONES PERSONALIZADAS ---
# ==============================================
# Importa nuestra función interna para establecer una conexión segura a la base de datos.
from custom_functions.security_engine import get_secure_engine

# Importa la configuración del sistema de registros (logs) para documentar el proceso.
from custom_functions.logging_pipeline import get_logging_pipeline

# Inicializa el registro de logs para documentar cada paso que da el pipeline.
get_logging_pipeline()

# ===================================================
# --- BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
# ===================================================
# Sube tres niveles desde este archivo para encontrar la carpeta raíz del proyecto.
base_dir = Path(__file__).resolve().parents[3]

# Define la ruta exacta en tu computadora donde se guardarán los reportes finales.
target_results_dir = base_dir / "05_results" / "rrhh" / "day09_base_aggregations"

# Registra el momento exacto en el que empieza el proceso para poder calcular la duración.
inicio_tiempo = time.time()


# ===================================================
# --- BLOQUE 4: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL ---
# ===================================================
def process_base_aggregations():
    # Informa que se está iniciando el intento de conexión con la base de datos PostgreSQL.
    print("\n")
    logging.info("🚀 ====== INICIANDO CONEXIÓN CON PostgreSQL ======")

    # Confirma que la conexión se estableció y calcula el tiempo que tardó.
    logging.info(
        "✅ Conexión con PostgreSQL establecida en %.2f segundos.",
        time.time() - inicio_tiempo,
    )

    try:
        # Llama a la función segura para conectarse a la base de datos.
        engine = get_secure_engine()

        # Consulta (Query) SQL que indica al sistema que extraiga toda la información de la vista de RRHH.
        query = """ SELECT * FROM view_hr_financial_snapshot """

        # Ejecuta la consulta SQL y guarda los resultados en una tabla de datos (DataFrame).
        df_agg = pd.read_sql(query, con=engine)

        # Verifica si la tabla de datos extraída no está vacía.
        if not df_agg.empty:
            logging.info("====== INICIA PROCESAMIENTO DE DATOS ======")

            # Informa que el programa ha comenzado a extraer la información financiera.
            logging.info(
                "⏳ Extrayendo resumen financiero desde la vista PostgreSQL..."
            )

            # Revisa si en la columna de nómina total existe algún valor menor o igual a cero.
            if (df_agg["total_payroll"] <= 0).any():
                # Si encuentra valores incorrectos (cero o negativos), marca un error crítico y detiene el proceso.
                logging.error(
                    "❌ CRÍTICO: Se detectaron departamentos con nómina igual o menor a cero."
                )
                return False
            else:
                # Si los datos son correctos, anuncia cuántas filas de información se recibieron.
                logging.info(
                    f"📊 Filas agregadas y recibidas de manera exitosa: {len(df_agg)}"
                )

                # Muestra en la consola una pequeña vista previa de los datos extraídos.
                print("\n 👀 Vista previa del talento de alto costo en ventas:")
                print(df_agg.head().to_string(index=False))

            try:
                # Crea la carpeta de destino en tu computadora si no existe todavía.
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Genera una marca de tiempo actual (AñoMesDía_HoraMinutoSegundo) para identificar el archivo.
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Construye el nombre final y la ruta completa que tendrá el archivo CSV.
                processed_file_name = (
                    f"day09_hr_financial_snapshot_backup_{time_stamp}.csv"
                )
                processed_path_name = target_results_dir / processed_file_name

                # Alerta al usuario que la escritura del archivo ha comenzado.
                print("\n")
                logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

                # Guarda los datos en tu disco duro en formato CSV, asegurando que los caracteres se lean bien universalmente (UTF-8).
                df_agg.to_csv(processed_path_name, index=False, encoding="utf-8")

                # Confirma que el archivo se guardó correctamente mostrando su ubicación.
                logging.info(
                    f"💾 Resultado exportado con éxito en: {target_results_dir}"
                )
                logging.info(f"📄 CSV: {processed_file_name}")
                print("\n")

            except Exception as e_export:
                # Captura y muestra cualquier error que ocurra al intentar guardar el archivo en la computadora.
                logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
                print("\n")

        else:
            # Informa en caso de que la consulta a la base de datos no haya devuelto ningún registro.
            logging.info("✨ No se encontraron registros que exportar.")

    except Exception as e:
        # Captura y muestra cualquier error general que ocurra en el proceso (ej. fallo al consultar la base de datos).
        logging.error(f"❌ Error en el proceso de validación: {e}")
        return False

    return True


# ===================================================
# --- BLOQUE 5: EJECUCIÓN PRINCIPAL DEL SCRIPT ---
# ===================================================
# Si este archivo se ejecuta directamente como programa principal, inicia el proceso de agregación.
if __name__ == "__main__":
    # Si el proceso falla en algún punto, el programa cierra indicando un error en el sistema.
    if not process_base_aggregations():
        sys.exit(1)
