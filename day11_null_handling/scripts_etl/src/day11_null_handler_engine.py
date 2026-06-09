# ==============================================================================
# Título: Pipeline Automatizado de Auditoría y Limpieza de Datos de Recursos
# Humanos
#
# Objetivo: Extraer datos brutos de la base de datos, corregir valores nulos y
# exportar un reporte limpio en CSV.
#
# Descripción: Este script actúa como un proceso ETL completo. Conecta de forma
# segura a una base de datos para traer la información de los empleados, audita
# cuántos registros están vacíos en el sistema, aplica reglas de negocio
# automatizadas para limpiar esos nulos (ingresos a 0 y desempeño a 99), valida
# mediante un control de calidad que no queden errores remanentes y, finalmente,
# exporta un archivo CSV con una estampa de tiempo única en una carpeta
# organizada por fechas.
#
# Archivo Python: day11_null_handler_engine.py
#
# Archivo CSV: day11_null_handler_engine.csv
#
# Archivo PNG: day11_null_handler_engine.png
# ==============================================================================

# ===========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas y utilidades necesarias para el programa.
# ===========================================================================
import pandas as pd  # Herramienta principal para manipular y estructurar datos en tablas.
import logging  # Para registrar y mostrar mensajes de estado durante la ejecución.
import sys  # Permite interactuar con el sistema operativo y las rutas de Python.
import os  # Proporciona funciones para interactuar con los comandos del sistema.
from pathlib import (
    Path,
)  # Facilita la creación y manipulación de rutas de carpetas de forma segura.
from datetime import (
    datetime,
)  # Nos da la fecha y hora exacta actual para nombrar los archivos.

# ==============================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO
# Objetivo: Asegurar que Python pueda encontrar todos los módulos del proyecto y
# definir rutas.
# ==============================================================================
# Busca la ruta de la carpeta del proyecto (un nivel arriba de este archivo).
src_dir = str(Path(__file__).resolve().parents[1])

# Si la ruta del proyecto no está registrada en Python, la insertamos al inicio del buscador.
if not src_dir in sys.path:
    sys.path.insert(0, src_dir)

# Importamos las herramientas de seguridad y mensajería propias de nuestra empresa.
from custom_functions.security_engine import get_secure_engine
from custom_functions.logging_pipeline import get_logging_pipeline

# Definimos de forma dinámica la ruta donde se guardarán los resultados (tres niveles arriba).
base_dir = Path(__file__).resolve().parents[3]
target_results_dir = base_dir / "05_results" / "rrhh" / "day11_null_handling"

# Activamos el sistema de bitácora/logs para ver el progreso del programa en consola.
get_logging_pipeline()


# ==============================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL DE AUDITORÍA Y LIMPIEZA
# Objetivo: Encapsular el proceso de extracción, limpieza, validación y guardado.
# ==============================================================================
def audit_and_input_nulls():
    try:
        # ======================================================
        # BLOQUE 3.1: CONEXIÓN Y EXTRACCIÓN
        # Objetivo: Conecta a la base de datos de manera segura.
        # ======================================================
        engine = get_secure_engine()

        # Diseñamos la consulta SQL para traer únicamente las 4 columnas de interés.
        query = """
            SELECT
                employee_id,
                employee_number,
                monthly_income,
                performance_rating
            FROM
                employee_master_dirty_data
        """

        # Ejecutamos la consulta y descargamos los datos en una tabla de memoria (DataFrame).
        df = pd.read_sql(query, con=engine)

        # Si la tabla contiene información, comenzamos el procesamiento.
        if not df.empty:
            print("\n")
            logging.info("====== INICIA PROCESAMIENTO DE DATOS ======")

            # =====================================================================
            # BLOQUE 3.2: AUDITORÍA INICIAL
            # Objetivo: Contamos cuántos valores vacíos (nulos) vinieron de origen.
            # =====================================================================
            null_income = int(df["monthly_income"].isna().sum())
            null_perf = int(df["performance_rating"].isna().sum())

            # Mostramos en el reporte el estado de salud inicial de los datos brutos.
            logging.info("====== AUDITORÍA INICIAL ======")
            logging.info(f"🔍 Nulos en Ingresos: {null_income}")
            logging.info(f"🔍 Nulos en Desempeño: {null_perf}")

            # ================================================================
            # BLOQUE 3.3: IMPUTACIÓN (LIMPIEZA)
            # Objetivo: Sustituimos los nulos por valores estándar de negocio.
            # ================================================================
            df["monthly_income"] = df["monthly_income"].fillna(
                0
            )  # Vacíos en salario se vuelven 0.
            df["performance_rating"] = df["performance_rating"].fillna(
                99
            )  # Vacíos en desempeño se vuelven 99.

            # ================================================================
            # BLOQUE 3.4: CONTROL DE CALIDAD
            # Objetivo: Verificación estricta de que el proceso funcionó.
            # ================================================================
            # Asegrar de que la condición sea totalmente cierta. Si no lo es,
            # el programa se detendrá automáticamente con una alerta.
            # Sintaxis: assert condicion_que_debe_ser_verdadera, "Mensaje de error personalizado"
            assert (
                df["monthly_income"].isna().sum() == 0
            ), "❌ Error: Quedaron nulos remanentes en ingresos."
            logging.info(
                "✅ Remoción completa de valores faltantes verificada con éxito."
            )

            # Imprimimos una pequeña muestra visual en la consola para confirmar el resultado.
            print("\n👀 Vista previa:")
            print(df.head())

            # ================================================================
            # BLOQUE 3.5: ALMACENAMIENTO
            # Objetivo: Guardado seguro del archivo final en el disco duro.
            # ================================================================
            try:
                # Si las carpetas de destino no existen en la computadora, las crea automáticamente.
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Creamos una marca de tiempo (AñoMesDía_HoraMinutoSegundo) para que el archivo sea único.
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Estructuramos el nombre oficial del archivo y su ruta completa de guardado.
                processed_file_name = f"day11_null_handler_engine_{time_stamp}.csv"
                processed_file_path = target_results_dir / processed_file_name

                print("\n")
                logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

                # Exportamos la información a un archivo CSV estándar, codificado en UTF-8 (para acentos y caracteres especiales).
                df.to_csv(processed_file_path, index=False, encoding="utf-8")

                # Informamos al usuario que el archivo está listo y guardado.
                logging.info(
                    f"💾 Resultado exportado con éxito en: {target_results_dir}"
                )
                logging.info(f"📄 CSV: {processed_file_name}")
                print("\n")
                return True

            # Si ocurre un problema exclusivo al intentar escribir el archivo en el disco, se captura aquí.
            except Exception as e_export:
                logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
                print("\n")
                return False

        # Si la consulta de la base de datos regresó completamente vacía, se salta la limpieza.
        else:
            logging.info("✨ No se encontraron registros para exportar.")
            print("\n")
            return False

    # Si ocurre un error crítico general (como fallos en la conexión de red con la base de datos), se captura aquí.
    except Exception as e:
        logging.error(f"❌ Falló la auditoría de nulos: {e}")
        print("\n")
        return False


# ==============================================================================
# BLOQUE 4: DISPARADOR AUTOMÁTICO (ENTRY POINT)
# Objetivo: Garantizar que el script solo se ejecute cuando sea invocado directamente.
# ==============================================================================
if __name__ == "__main__":
    # Ejecutamos nuestra función principal. Si el pipeline reporta un fallo, cierra el programa enviando una señal de error (1) al sistema.
    if not audit_and_input_nulls():
        sys.exit(1)
