# =====================================================================
# Título: Pipeline de Sincronización y Segmentación de Riesgo de RRHH
#
# Objetivo: Clasificar de forma automática el nivel de riesgo de
# deserción o desgaste laboral de los empleados basándose en sus horas
# extra y su balance de vida actual.
#
# Descripción: Este script se conecta de manera segura a una base de
# datos PostgreSQL para extraer la información vigente de los empleados.
# Posteriormente, aplica reglas lógicas de negocio para etiquetar a cada
# trabajador en una categoría de riesgo (Alto, Moderado o Bajo).
# Finalmente, exporta los resultados actualizados en dos archivos CSV
# (uno maestro y un respaldo con la fecha y hora exacta del proceso)
# dentro de una carpeta centralizada de Recursos Humanos.
#
# Archivo Python: day14_pipeline_sincronizacion.py
#
# Archivo CSV: day14_attrition_procesado.csv
#
# Archivo PNG: day14_pipeline_sincronizacion.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para el programa.
# =====================================================================
# Pandas nos ayuda a manipular y organizar los datos en tablas (DataFrames)
import pandas as pd

# Sys nos permite interactuar directamente con el sistema operativo
import sys

# Logging sirve para guardar un registro de lo que pasa en el programa
import logging

# Numpy nos ayuda a realizar operaciones lógicas y matemáticas rápidas
import numpy as np

# Datetime nos ayuda a obtener la fecha y hora actual para los respaldos
from datetime import datetime

# Path nos ayuda a manejar rutas de archivos sin importar el sistema operativo
from pathlib import Path

# =====================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que el programa sepa dónde buscar carpetas.
# =====================================================================
# Buscamos la carpeta contenedora del script para que el sistema la reconozca
src_dir = str(Path(__file__).resolve().parents[1])

# Si esa carpeta no está en la lista de rutas de Python, la agregamos aquí
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos funciones creadas por nuestro equipo para seguridad y registros
from custom_functions.security_engine import get_secure_engine
from custom_functions.logging_pipeline import get_logging_pipeline

# Calculamos la ruta de la carpeta raíz del proyecto subiendo 3 niveles
base_dir = Path(__file__).resolve().parents[3]

# Definimos la carpeta exacta donde guardaremos los reportes de RRHH
target_results_dir = base_dir / "05_results" / "rrhh" / "day14_synchronization"

# Encendemos nuestro sistema de registro (bitácora) para el pipeline
get_logging_pipeline()


# ==============================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL Y PROCESAMIENTO
# Objetivo: Conectarse a la fuente principal (PostgreSQL), procesamiento y
# exportación de datos.
# ==============================================================================
def procesar_segmentación():
    # Dejamos un espacio en blanco en la consola por orden visual
    print("\n")
    # Registramos que estamos listos para conectarnos a la base de datos
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Obtenemos la conexión segura a la base de datos
        engine = get_secure_engine()

        # Escribimos la consulta SQL para traer los datos de retención laboral
        query = """
            SELECT *
            FROM view_employee_retention_data
        """

        # Ejecutamos la consulta y guardamos la información en una tabla de Pandas
        df = pd.read_sql(query, con=engine)

        # Si la tabla contiene información (no está vacía), iniciamos el análisis
        if not df.empty:
            logging.info("🚀 ==== INICIA PROCESAMIENTO DE DATOS ====")

            # Definición de la matriz de riesgo lógico operativo.
            # Riesgo Alto: Hace horas extra y tiene bajo balance de vida.
            # Riesgo Medio: Hace horas extra o tiene bajo balance de vida.
            condiciones = [
                (df["horas_extra"] == "Yes") & (df["balance_vida"].isin([1, 2])),
                (df["horas_extra"] == "Yes") | (df["balance_vida"].isin([1, 2])),
            ]

            # Estas son las etiquetas que corresponden a las condiciones anteriores
            opciones = ["1 - Alto Riesgo", "2 - Riesgo Moderado"]

            # Creamos la nueva columna asignando el riesgo, por defecto será "Bajo"
            df["matriz_riesgo"] = np.select(
                condiciones, opciones, default="3 - Riesgo Bajo"
            )

            print("\n👀 Vista previa: ")
            print(df.head())

            # ==============================================================================
            # BLOQUE 4: EXPORTACIÓN SEGURA A FORMATO CSV.
            # Objetivo: Guardamos físicamente los resultados para garantizar que no se
            # pierdan los datos.
            # ==============================================================================
            try:
                # Si la carpeta de destino no existe, la creamos en este momento
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Creamos una marca de tiempo con formato AñoMesDía_HoraMinutoSegundo
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Definimos el nombre y la ruta del archivo maestro actualizado
                processed_file_name = "day14_attrition_procesado.csv"
                processed_file_path = target_results_dir / processed_file_name

                # Definimos el nombre y ruta del archivo de respaldo (histórico)
                processed_bakup_file_name = (
                    f"day14_pipeline_sinconizacion_{time_stamp}.csv"
                )
                processed_bakup_file_path = (
                    target_results_dir / processed_bakup_file_name
                )

                print("\n")
                logging.info("🚀 ==== INICIA EXPORTACIÓN DE DATOS A CSV ====")

                # Guardamos los datos en el archivo maestro (sobrescribe el anterior)
                df.to_csv(processed_file_path, index=False, encoding="UTF-8")
                # Guardamos los mismos datos en el archivo de respaldo único
                df.to_csv(processed_bakup_file_path, index=False, encoding="UTF-8")

                # Avisamos en la bitácora que todo se guardó correctamente
                logging.info(
                    f"💾 Snapshot de control guardado con {len(df)} registros procesados"
                )
                logging.info(
                    f"💾 Resultado exportado con éxito en: {target_results_dir}"
                )
                logging.info(f"📄 CSV Maestro: {processed_file_name}")
                logging.info(f"📄 CSV Respaldo (Backup): {processed_bakup_file_name}")
                print("\n")
                return True

            # Si algo falla al guardar los archivos CSV, capturamos el error aquí
            except Exception as e_export:
                logging.info(f"❌ Alerta - No se pudo exportar el archivo: {e_export}")
                print("\n")
                return False

        # Si la tabla llegó vacía desde la base de datos, avisamos aquí.
        else:
            logging.info("✨ No se encontraron registros.")
            print("\n")
            return False

    # Si ocurre un error general (conexión, lectura, etc.), lo atrapamos aquí
    except Exception as e:
        logging.info(f"❌ Error detectado en: {e}")
        return False


# =====================================================================
# BLOQUE 5: DISPARADOR DEL PROGRAMA
# Objetivo: Asegurar que el script corra solo si lo ejecutamos directo.
# =====================================================================
# Este bloque asegura que el código se ejecute solo si abrimos este script directamente
if __name__ == "__main__":
    # Ejecutamos la función principal; si da error (False), cerramos el programa
    if not procesar_segmentación():
        sys.exit(1)
