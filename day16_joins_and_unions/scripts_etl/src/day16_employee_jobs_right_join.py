# =====================================================================
# Título: Pipeline para Auditoría y Combinación de Puestos y Empleados
#
# Objetivo: Conectar a PostgreSQL, extraer empleados y puestos, y
# cruzarlos garantizando conservar todos los puestos de trabajo.
#
# Descripción: Este programa consulta la información de empleados y
# puestos laborales. Utiliza una combinación de tipo "Right Join"
# tomando como catálogo base la tabla de puestos (derecha). Esto
# permite verificar si existen puestos registrados que no tengan
# empleados asignados.
#
# Archivo Python: day16_employee_jobs_right_join.py
#
# Archivo PNG; day16_employee_jobs_right_join.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para el programa.
# =====================================================================
# Pandas nos ayuda a manipular y organizar datos en tablas fácilmente.
import pandas as pd

# Sys nos permite interactuar directamente con el sistema operativo.
import sys

# Logging sirve para registrar mensajes de avance o errores.
import logging

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

# Importamos una función para configurar el registro de mensajes.
from custom_functions.logging_pipeline import get_logging_pipeline

# Importamos la herramienta para conectarnos de forma segura a la BD.
from custom_functions.security_engine import get_secure_engine

# Activamos el sistema de registros de mensajes del programa.
get_logging_pipeline()


def right_join():
    """Realiza la extracción de datos y la combinación de las tablas."""

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

        # Traemos la información de empleados y la guardamos en una tabla.
        df_fact_employees = pd.read_sql(query_1, con=engine)

        # Traemos la información de puestos y la guardamos en otra tabla.
        df_dim_jobs = pd.read_sql(query_2, con=engine)

        # Verificamos si la tabla principal de empleados contiene datos.
        if not df_fact_employees.empty:

            # Verificamos si la tabla secundaria de puestos tiene datos.
            if not df_dim_jobs.empty:

                # Avisamos que inicia la combinación de la información.
                logging.info("====⚡ INICIA PROCESAMIENTO DE DATOS (RIGHT JOIN) ====")

                # Unimos ambas tablas priorizando la tabla de puestos
                # (derecha) mediante la columna clave "job_id".
                df_resultado = pd.merge(
                    left=df_fact_employees, right=df_dim_jobs, on="job_id", how="right"
                )

                # Definimos las columnas específicas que queremos visualizar.
                columnas_deseadas = [
                    "employee_number",
                    "monthly_income",
                    "job_role",
                    "department",
                ]

                # Mostramos en pantalla los primeros registros combinados.
                print("\n👀 Vista previa: ")
                print(df_resultado[columnas_deseadas].head())

                print("\n")
                return True

            else:
                # Avisamos si la tabla de puestos está vacía y frenamos.
                logging.info(
                    "❌ No se encontraron registros en la tabla "
                    "secundaria (derecha)."
                )
                return False
        else:
            # Avisamos si la tabla de empleados está vacía y frenamos.
            logging.info(
                "❌ No se encontraron registros en la tabla principal " "(izquierda)."
            )
            return False

    except Exception as e:
        # Registramos cualquier falla imprevista durante la ejecución.
        logging.error(f"❌ Error detectado en: {e}")
        return False


# Punto de entrada principal: se ejecuta solo si llamamos a este script.
if __name__ == "__main__":
    # Ejecutamos la función. Si retorna un fallo (False), cerramos.
    if not right_join():
        sys.exit(1)
