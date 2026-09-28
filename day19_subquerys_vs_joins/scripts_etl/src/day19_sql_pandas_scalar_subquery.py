# =========================================================================
# Título: Consulta SQL de Empleados con Salario Superior al Promedio
#
# Objetivo: Ejecutar una consulta SQL mediante SQLAlchemy para filtrar
# a los empleados cuyo ingreso mensual sea mayor al promedio general.
#
# Descripción: El pipeline establece una conexión segura con PostgreSQL,
# envía una consulta SQL que calcula una subconsulta escalar para el
# promedio salarial y une la tabla de empleados con la dimensión de
# puestos, devolviendo el resultado ordenado en un DataFrame.
#
# Archivo Python: day19_sql_pandas_scalar_subquery.py
#
# Archivo PNG: day19_sql_pandas_scalar_subquery.png
# =========================================================================

# =========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y ajustar las rutas del sistema.
# =========================================================================

# Manipulación de datos
import pandas as pd

# Control del sistema y script
import sys

# Registro de eventos y logs
import logging

# Gestión de rutas de archivos
from pathlib import Path

# Ejecución de SQL plano en SQLAlchemy
from sqlalchemy import text

# Obtener e incluir la ruta raíz del proyecto
src_dir = str(Path(__file__).resolve().parents[1])
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Conexión segura y sistema de logs
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Inicializar logs
get_logging_pipeline()

# =========================================================================
# BLOQUE 2: DEFINICIÓN DEL PIPELINE Y EJECUCIÓN DE LA CONSULTA SQL
# Objetivo: Conectar a la base de datos, ejecutar la consulta y mostrar.
# =========================================================================


def sqlalchemy_scalar_sq() -> bool:
    """Ejecuta consulta SQL directa con subconsulta escalar para obtener

    empleados cuyo salario sea superior al promedio.
    """
    print("\n")
    logging.info("🚀==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Motor seguro de conexión
        engine = get_secure_engine()

        # Consulta SQL con CTE y subconsulta escalar
        query_sql_scalar = text("""
        -- =================================================================
        -- BLOQUE 3: CÁLCULO DEL PROMEDIO SALARIAL GLOBAL (CTE)
        -- Objetivo: Crear una tabla temporal con el sueldo promedio.
        -- =================================================================

        -- CTE para calcular el promedio de ingreso mensual
        WITH avg_monthly_income AS (
            SELECT
                AVG(monthly_income)
            FROM
                fact_employees
        )

        -- =================================================================
        -- BLOQUE 4: SELECCIÓN Y FILTRADO DE EMPLEADOS SUPERIORES
        -- Objetivo: Consultar empleados sobre el promedio y ordenar.
        -- =================================================================

        -- Selección de atributos clave
        SELECT
            employee_number,
            j.department,
            j.job_role,
            monthly_income

        -- Tabla principal de empleados
        FROM fact_employees AS e

        -- Cruce con catálogo de puestos
        INNER JOIN dim_jobs AS j
            ON e.job_id = j.job_id

        -- Filtro contra valor escalar de la CTE
        WHERE
            monthly_income > (
                SELECT *
                FROM
                    avg_monthly_income
            )

        -- Ordenamiento descendente por ingreso
        ORDER BY
            monthly_income DESC;
        """)

        # Abrir conexión
        with engine.connect() as conexion:
            # Ejecutar consulta SQL y guardar resultado en DataFrame
            df_resultado_sql = pd.read_sql_query(query_sql_scalar, con=conexion)

            # Validar si el DataFrame contiene datos
            if not df_resultado_sql.empty:
                logging.info(
                    "⚙️ ==== INICIANDO PROCESAMIENTO Y LÓGICA INTEGRADA "
                    "DE NEGOCIO ===="
                )
                print("\n✅ Datos cargados exitosamente.")
                print(
                    "\n==== RESULTADO SQL + SQLALCHEMY "
                    "Empleados con Salario > Promedio ===="
                )

                # Mostrar total y vista previa
                total_filas = len(df_resultado_sql)
                print(f"\nTotal de registros encontrados: {total_filas}")
                print("\n👀 Vista Previa:")
                print(df_resultado_sql.head().to_string(index=False))
                print("\n")

                # Liberar recursos y finalizar
                engine.dispose()
                return True

            else:
                # Alerta si la consulta no devuelve registros
                logging.info("❌ No se encontraron registros en la tabla.")
                print("\n")
                return False

    except Exception as e:
        # Registro de error y salida de emergencia
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =========================================================================
# BLOQUE 5: PUNTO DE ENTRADA Y EJECUCIÓN PRINCIPAL
# Objetivo: Iniciar el flujo de trabajo cuando se ejecuta este archivo.
# =========================================================================

if __name__ == "__main__":
    # Iniciar flujo principal
    df_sqlalchemy_scalar_sq = sqlalchemy_scalar_sq()

    # Validar código de salida
    if isinstance(df_sqlalchemy_scalar_sq, bool) and not df_sqlalchemy_scalar_sq:
        sys.exit(1)
