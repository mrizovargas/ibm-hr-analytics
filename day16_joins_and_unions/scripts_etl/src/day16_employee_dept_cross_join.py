# =====================================================================
# Título: Matriz de Evaluación de Empleados y Departamentos
#
# Objetivo: Generar una matriz de evaluación que combine a cada uno de
# los empleados con los diferentes departamentos de la empresa.
#
# Descripción: Este script se conecta a la base de datos PostgreSQL,
# extrae los registros de empleados y puestos, obtiene la lista única
# de departamentos y realiza un cruce total (Cross Join) entre los datos
# clave de los empleados y dichos departamentos para posterior
# simulación.
#
# Archivo Python: day16_employee_dept_cross_join.sql
#
# Archivo PNG: day16_employee_dept_cross_join.png
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


# =====================================================================
# BLOQUE 3: EXTRACCIÓN Y PROCESAMIENTO DE DATOS
# Objetivo: Consultar la BD y cruzar los empleados con departamentos.
# =====================================================================


def cross_join():
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

        # Traemos información de empleados y la guardamos en una tabla.
        df_fact_employees = pd.read_sql(query_1, con=engine)

        # Traemos información de puestos y la guardamos en otra tabla.
        df_dim_jobs = pd.read_sql(query_2, con=engine)

        # Verificamos si la tabla principal de empleados contiene datos.
        if not df_fact_employees.empty:

            # Verificamos si la tabla secundaria de puestos tiene datos.
            if not df_dim_jobs.empty:

                # Avisamos que inicia la combinación de la información.
                logging.info(
                    "====⚡ INICIA PROCESAMIENTO DE DATOS " "(CROSS JOIN) ===="
                )

                # Extraemos la lista de departamentos sin repetirlos.
                df_deptos = df_dim_jobs[["department"]].drop_duplicates()

                # Cruzamos cada empleado con todos los departamentos.
                df_matriz_evaluacion = pd.merge(
                    left=df_fact_employees[["employee_number", "monthly_income"]],
                    right=df_deptos,
                    how="cross",
                )

                # Imprimimos el conteo total de filas generadas.
                total_filas = len(df_matriz_evaluacion)
                print(
                    f"\nTotal Matriz DataFrame: La matriz contiene "
                    f"un total de {total_filas} filas registradas."
                )

                # Mostramos en pantalla los primeros registros combinados.
                print("\n👀 Vista previa: ")
                print(df_matriz_evaluacion.head())

                print("\n")
                return True

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
    # Ejecutamos la función. Si retorna un fallo (False), cerramos.
    if not cross_join():
        sys.exit(1)
