# =====================================================================
# Título: Validación de combinación de tablas y tiempo de ejecución en
# Python
#
# Objetivo: Medir el rendimiento y verificar la integridad de datos al
# realizar una unión de tablas directamente en memoria local.
#
# Descripción: El script extrae las tablas de empleados y puestos desde
# PostgreSQL, realiza un cruce mediante Pandas, mide el tiempo que toma
# el proceso y confirma que se mantengan exactamente 3,000 registros.
#
# Archivo Python: day16_validate_join_preservation.py
#
# Archivo PNG: day16_validate_join_preservation.png
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


def validate_join_preservation():
    """Conecta a la BD, combina tablas en Python y mide el tiempo."""

    # Imprimimos una línea en blanco para dar espacio visual en consola.
    print("\n")

    # Notificamos que vamos a iniciar la conexión con PostgreSQL.
    logging.info("🚀 ==== INICIAMOS CONEXIÓN CON POSTGRESQL ====")

    # Intentamos ejecutar el proceso y capturamos fallos si ocurren.
    try:
        # Creamos la llave de acceso seguro hacia la base de datos.
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

                # Unimos ambas tablas mediante la clave de puesto común.
                df_merged = pd.merge(
                    left=df_fact_employees,
                    right=df_dim_jobs,
                    on="job_id",
                    how="inner",
                )

                # Detenemos el cronómetro al finalizar el procesamiento.
                end_time = time.perf_counter()

                # Convertimos la diferencia de tiempo a milisegundos.
                execution_time = (end_time - start_time) * 1000

                # Definimos las columnas requeridas para la vista final.
                columnas_deseadas = [
                    "employee_number",
                    "monthly_income",
                    "job_id",
                    "job_role",
                    "department",
                ]

                # Imprimimos la cantidad de registros y el tiempo usado.
                print(
                    f"📊 Registros resultantes en memoria (Tabla Principal): "
                    f"{len(df_fact_employees)}"
                )
                print(
                    f"📊 Registros resultantes en memoria después del INNER JOIN (Tabla Secundaria): "
                    f"{len(df_merged)}"
                )
                print(f"⏱️ Tiempo de procesamiento local: " f"{execution_time:.4f} ms")

                # Validamos que el total de registros sea de 3,000 filas.
                assert len(df_merged) == len(df_fact_employees), (
                    f"\nError: Se detectaron {len(df_merged)} filas "
                    f"en lugar de {len(df_fact_employees)}"
                )

                # Confirmamos que la unión preservó la integridad.
                print(
                    "\n✅ Éxito: La combinación de tablas en Python "
                    f"mantiene la integridad de los {len(df_fact_employees)} empleados."
                )

                print("\n")
                return df_merged

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

    # Ejecutamos la función principal y guardamos el resultado obtenido.
    df_resultado = validate_join_preservation()

    # Si la validación falla o regresa vacío, detenemos la ejecución.
    if df_resultado is False or df_resultado.empty:
        sys.exit(1)
