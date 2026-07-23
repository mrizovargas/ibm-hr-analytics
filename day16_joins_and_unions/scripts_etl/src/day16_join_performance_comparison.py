# =====================================================================
# Título: Comparación de Rendimiento en Procesamiento de Joins
#
# Objetivo: Medir el tiempo exacto que le toma a Python unir dos tablas
# y filtrar registros directamente en la memoria local.
#
# Descripción: Este script se conecta a PostgreSQL para extraer las
# tablas de empleados y puestos, las une en memoria mediante un Inner
# Join utilizando Pandas, filtra únicamente al departamento de Ventas y
# calcula el tiempo preciso de ejecución en milisegundos.
#
# Archivo Python: day16_join_performance_comparison.py
#
# Archivo PNG: day16_join_performance_comparison.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para ejecutar el programa.
# =====================================================================

# Pandas nos ayuda a manipular y organizar datos en tablas fácilmente.
import pandas as pd

# Sys nos permite interactuar directamente con el sistema operativo.
import sys

# Logging sirve para registrar mensajes de avance o errores del flujo.
import logging

# Time nos permite tomar lecturas precisas de tiempo de procesamiento.
import time

# Path nos ayuda a gestionar rutas de archivos de manera sencilla.
from pathlib import Path

# =====================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que el programa sepa dónde buscar carpetas.
# =====================================================================

# Identificamos la carpeta raíz del proyecto para localizar módulos.
src_dir = str(Path(__file__).resolve().parents[1])

# Si la carpeta no está registrada en el sistema, la agregamos.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos la herramienta para conectarnos de forma segura a la BD.
from custom_functions.security_engine import get_secure_engine

# Importamos una función para configurar el registro de mensajes.
from custom_functions.logging_pipeline import get_logging_pipeline

# Activamos el sistema de registros de mensajes del programa.
get_logging_pipeline()


# =====================================================================
# BLOQUE 3: EXTRACCIÓN Y MEDICIÓN DE RENDIMIENTO
# Objetivo: Consultar datos, realizar la unión, filtrar y medir tiempo.
# =====================================================================


def compare_join_performance():
    """Conecta a la BD, combina tablas en Python y mide el tiempo."""

    # Imprimimos una línea en blanco para dar espacio visual en consola.
    print("\n")

    # Notificamos que vamos a iniciar la conexión con PostgreSQL.
    logging.info("🚀 ==== INICIAMOS CONEXIÓN CON POSTGRESQL ====")

    # Intentamos ejecutar el proceso y capturamos fallos si ocurren.
    try:
        # Creamos el puente o llave de acceso seguro a la base de datos.
        engine = get_secure_engine()

        # Preparamos la consulta para obtener a todos los empleados.
        query_1 = """
            SELECT *
            FROM fact_employees;
        """

        # Preparamos la consulta para obtener el catálogo de puestos.
        query_2 = """
            SELECT *
            FROM dim_jobs;
        """

        # Traemos información de empleados y la guardamos en una tabla.
        df_fact_employees = pd.read_sql(query_1, con=engine)

        # Traemos información de puestos y la guardamos en otra tabla.
        df_dim_jobs = pd.read_sql(query_2, con=engine)

        # Verificamos si la tabla principal de empleados contiene datos.
        if not df_fact_employees.empty:

            # Verificamos si la tabla secundaria de puestos tiene datos.
            if not df_dim_jobs.empty:

                # Avisamos el inicio de la prueba de rendimiento.
                logging.info("🚀 ==== MINDSET DE OPTIMIZACIÓN ====")
                print("\n⚡ Iniciando comparación de procesamiento en " "Python...")

                # Iniciamos un cronómetro de alta precisión.
                start_time = time.perf_counter()

                # Unimos ambas tablas conservando coincidencias exactas.
                df_merged = pd.merge(
                    left=df_fact_employees,
                    right=df_dim_jobs,
                    on="job_id",
                    how="inner",
                )

                # Conservamos únicamente los empleados de 'Sales'.
                df_filtered = df_merged[df_merged["department"] == "Sales"]

                # Detenemos el cronómetro al finalizar el procesamiento.
                end_time = time.perf_counter()

                # Convertimos la diferencia de tiempo a milisegundos.
                execution_time = (end_time - start_time) * 1000

                # Definimos las columnas requeridas para la vista.
                columnas_deseadas = [
                    "employee_number",
                    "monthly_income",
                    "job_id",
                    "job_role",
                    "department",
                ]

                # Imprimimos la cantidad de registros y el tiempo usado.
                print(f"📊 Registros resultantes en memoria: " f"{len(df_filtered)}")
                print(f"⏱️ Tiempo de procesamiento local: " f"{execution_time:.4f} ms")

                # Mostramos en pantalla los primeros registros.
                print("\n👀 Vista previa: ")
                print(df_filtered[columnas_deseadas].head())

                print("\n")
                return df_filtered

            else:
                # Avisamos si la tabla de puestos está vacía y frenamos.
                logging.info(
                    "❌ No se encontraron registros en la tabla "
                    "secundaria (derecha)."
                )
                print("\n")
                return False
        else:
            # Avisamos si la tabla de empleados está vacía y frenamos.
            logging.info(
                "❌ No se encontraron registros en la tabla " "principal (izquierda)."
            )
            print("\n")
            return False

    except Exception as e:
        # Registramos cualquier falla imprevista durante la ejecución.
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        return False


# =====================================================================
# BLOQUE 4: PUNTO DE ENTRADA PRINCIPAL
# Objetivo: Controlar la ejecución directa del script desde consola.
# =====================================================================

# Punto de entrada principal: se ejecuta solo si llamamos a este script.
if __name__ == "__main__":
    # Ejecutamos la función y guardamos el resultado
    df_resultado = compare_join_performance()

    # Si el DataFrame está vacío, lo consideramos un fallo y cerramos
    if df_resultado.empty:
        sys.exit(1)
