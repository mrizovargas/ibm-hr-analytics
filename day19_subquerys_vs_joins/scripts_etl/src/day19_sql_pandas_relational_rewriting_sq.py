# =====================================================================
# Título: Evaluación de Consultas SQL (Subconsulta vs INNER JOIN)
#
# Objetivo: Comparar la ejecución de una subconsulta ineficiente contra
# un JOIN.
#
# Descripción: Conecta a PostgreSQL y ejecuta dos estrategias de consulta
# para obtener datos de empleados del área de ventas.
#
# Archivo Python: day19_sql_pandas_relational_rewriting_sq.py
#
# Archivo PNG: day19_sql_pandas_relational_rewriting_sq.png
# =====================================================================


# =====================================================================
# BLOQUE 1: Importación de librerías y preparación del entorno
# Objetivo: Cargar librerías y configurar rutas del sistema
# =====================================================================

# Registro de eventos y logs
import logging

# Gestión de rutas de archivos
from pathlib import Path

# Control del sistema y script
import sys

# Manipulación de datos
import pandas as pd

# Procesamiento de texto SQL
from sqlalchemy import text

# Añadimos la carpeta raíz al camino de búsqueda del sistema
src_dir = str(Path(__file__).resolve().parents[1])
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos funciones personalizadas del proyecto
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Inicializamos el sistema de logs
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: Evaluación de consultas e interacción con la base de datos
# Objetivo: Conectar a PostgreSQL, consultar datos y validar resultados
# =====================================================================
def evaluate_join_performance() -> bool:
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    # Creamos el motor de conexión
    engine = get_secure_engine()

    # =================================================================
    # PASO 1: Consulta Ineficiente usando una Subconsulta (WHERE IN)
    # =================================================================

    # Selecciona campos buscando IDs con filtro WHERE IN
    inefficient_sql_query = text("""
        SELECT
            e.employee_number, -- Número de empleado (tabla principal)
            e.job_id,          -- Identificador del puesto
            e.monthly_income   -- Salario mensual
        FROM
            fact_employees AS e -- Tabla principal de empleados
        WHERE
            e.job_id IN(        -- Filtra puestos presentes en la lista
                SELECT
                    j.job_id
                FROM
                    dim_jobs AS j -- Tabla secundaria de puestos
                WHERE
                    j.department = 'Sales' -- Filtro por departamento
            );
    """)

    try:
        # Ejecutamos la consulta ineficiente
        with engine.connect() as conn:
            inefficient_df = pd.read_sql_query(inefficient_sql_query, conn)

            if not inefficient_df.empty:
                logging.info(
                    "🚀 ==== INICIANDO PROCESAMIENTO DE DATOS Y LÓGICA DE"
                    " NEGOCIO (Subconsulta WHERE IN) ===="
                )
                print("\n✅ Carga de datos exitosa.")

                inefficient_total_records = len(inefficient_df)

                print("==== RESULTADO INEFICIENTE (Subconsulta WHERE IN) ====")
                print(
                    "\n📊 Total de registros encontrados:"
                    f" {inefficient_total_records}"
                )
                print("\n👀 Vista Previa:")
                print(inefficient_df.head().to_string(index=False))
                print("\n")

            else:
                print("\n")
                logging.warning("⚠️ La consulta SQL no arrojó ningún resultado.")

    except Exception as e:
        # Captura y registro de errores en la primera consulta
        message_error = getattr(e, "orig", e)
        logging.error(f"❌ Error detectado en: {message_error}")
        print("\n")
        sys.exit(1)

    finally:
        # Liberación de recursos de conexión
        engine.dispose()
        logging.info("🔒 Motor de conexión liberado.")

    # =================================================================
    # PASO 2: Consulta Optimizada usando un INNER JOIN Relacional
    # =================================================================

    # Combina tablas directamente por clave compartida
    optimized_sql_query = text("""
        SELECT
            e.employee_number, -- Número de empleado
            j.department,      -- Departamento de trabajo
            j.job_role,        -- Nombre del puesto
            e.monthly_income   -- Salario mensual
        FROM
            fact_employees as e -- Tabla principal
        INNER JOIN
            dim_jobs as j      -- Cruce directo con la tabla de puestos
                ON e.job_id = j.job_id -- Condición de cruce por clave
        WHERE
            j.department = 'Sales';    -- Filtro de departamento objetivo
    """)

    try:
        # Ejecutamos la consulta optimizada
        with engine.connect() as conn:
            optimized_df = pd.read_sql_query(optimized_sql_query, conn)

            if not optimized_df.empty:
                logging.info(
                    "🚀 ==== INICIANDO PROCESAMIENTO DE DATOS Y LÓGICA DE"
                    " NEGOCIO (INNER JOIN Optimizado) ===="
                )

                print("\n✅ Carga de datos exitosa.")

                optimized_total_records = len(optimized_df)

                print(
                    "\n==== RESULTADO OPTIMIZADO (Reescritura Relacional"
                    " INNER JOIN) ===="
                )
                print(
                    "\n📊 Total de registros encontrados:" f" {optimized_total_records}"
                )
                print("\n👀 Vista Previa:")
                print(optimized_df.head().to_string(index=False))
                print("\n")

                # =====================================================================
                # PASO 3: Análisis del plan de ejecución en PostgreSQL
                # Objetivo: Inspeccionar los pasos internos que realiza la base de datos
                # =====================================================================

                # Anteponemos EXPLAIN a la consulta optimizada para ver cómo se ejecuta
                query_explain = text("EXPLAIN " + optimized_sql_query.text)

                # Nos conectamos a PostgreSQL y obtenemos el reporte del plan
                with engine.connect() as conexion:
                    plan_ejecucion = pd.read_sql_query(query_explain, conexion)

                # Imprimimos el resultado del plan en la consola
                print("--- PLAN DE EJECUCIÓN OPTIMIZADO ---")
                print(plan_ejecucion)

                return True

            else:
                print("\n")
                logging.warning("⚠️ La consulta SQL no arrojó ningún resultado.")

                return False

    except Exception as e:
        # Captura y registro de errores en la segunda consulta
        message_error = getattr(e, "orig", e)
        logging.error(f"❌ Error detectado en: {message_error}")
        print("\n")
        sys.exit(1)

    finally:
        # Liberación final de la conexión
        engine.dispose()
        logging.info("🔒 Motor de conexión liberado.")


# =====================================================================
# BLOQUE 3: Punto de entrada del script
# Objetivo: Controlar la ejecución del programa y su código de salida
# =====================================================================
if __name__ == "__main__":
    execution_result = evaluate_join_performance()

    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)

    else:
        logging.info("✅ Proceso finalizado exitosamente.")
        print("\n")
        sys.exit(0)
