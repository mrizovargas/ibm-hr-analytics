# =========================================================================
# Título: Consulta Correlacionada de Empleados en Puestos de Alto Riesgo
#
# Objetivo: Identificar empleados en roles con alta rotación usando SQL
# puro.
#
# Descripción: Conecta a PostgreSQL, ejecuta una consulta con subconsulta
# correlacionada y muestra el resumen de los resultados obteniendo los
# datos directamente en un DataFrame.
#
# Archivo Python: day19_sql_pandas_correlated_subquery.py
#
# Archivo PNG: day19_sql_pandas_correlated_subquery.png
# =========================================================================

# =========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar módulos necesarios y agregar rutas del proyecto.
# =========================================================================

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

# Agregar ruta raíz del proyecto al sistema
src_dir = str(Path(__file__).resolve().parents[1])
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Importación de funciones personalizadas de logs y seguridad
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Inicializar sistema de logs
get_logging_pipeline()

# =========================================================================
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DEL PIPELINE
# Objetivo: Preparar la consulta SQL y ejecutar la extracción.
# =========================================================================


def sql_correlated_subquery() -> bool:
    """Ejecuta consulta SQL correlacionada y retorna estado de éxito."""
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    # Motor seguro de conexión
    engine = get_secure_engine()

    # Consulta SQL con CTE y subconsulta correlacionada
    sql_correlated_query = text(
        """
        -- CTE: Filtrar puestos con alto riesgo de rotación
        WITH puestos_alto_riesgo AS (
            SELECT
                job_id
            FROM
                dim_jobs
            WHERE
                high_turnover_risk = 'Yes'
        )

        -- Consulta principal: Atributos clave del empleado
        SELECT
            e.employee_number,
            j1.department,
            j1.job_role,
            e.monthly_income

        -- Tabla principal de empleados
        FROM fact_employees AS e

        -- Cruce con catálogo de puestos para atributos descriptivos
        INNER JOIN dim_jobs AS j1
            ON j1.job_id = e.job_id

        -- Filtro de existencia en CTE de alto riesgo
        WHERE EXISTS (
            SELECT 1
            FROM
                puestos_alto_riesgo AS p
            WHERE
                p.job_id = e.job_id
        );
        """
    )

    try:
        # =================================================================
        # BLOQUE 3: EXTRACCIÓN Y EJECUCIÓN DE CONSULTA SQL
        # Objetivo: Obtener la información requerida directamente a Pandas.
        # =================================================================

        # Conectar a la BD y cargar datos en DataFrame
        with engine.connect() as conexion:
            df_resultado_final = pd.read_sql_query(
                sql_correlated_query, conexion
            )

        # =================================================================
        # BLOQUE 4: VALIDACIÓN Y DESPLIEGUE DE RESULTADOS
        # Objetivo: Confirmar datos y mostrarlos en pantalla.
        # =================================================================

        # Validar si se obtuvieron registros
        if not df_resultado_final.empty:
            logging.info(
                "🚀 ==== INICIANDO PROCESAMIENTO DE DATOS Y 'LÓGICA DE "
                "NEGOCIO' ===="
            )
            print("✅ Carga de datos exitosa.")

            # Total de registros extraídos
            total_filas = len(df_resultado_final)

            # Despliegue de resultados en consola
            print(
                "\n===== RESULTADO SQL PURO (Procesamiento Vectorizado + "
                "Pandas + Conexión SQLAlchemy) ===="
            )
            print(f"\n📊 Total de registros encontrados: {total_filas}")
            print("\n👀 Vista Previa:")
            print(df_resultado_final.head().to_string(index=False))
            print("\n")
            return True

        else:
            # Notificar búsqueda sin coincidencias
            print("\n")
            logging.warning(
                "⚠️ No se encontraron registros en la(s) tabla(s)."
            )
            return False

    except Exception as e:
        # Registrar error inesperado y detener ejecución
        message_error = getattr(e, "orig", e)
        logging.error(f"❌ Error detectado en: {message_error}")
        print("\n")
        sys.exit(1)

    finally:
        # Liberar recursos del motor
        engine.dispose()
        logging.info("🔒 Motor de conexión liberado.")


# =========================================================================
# BLOQUE 5: PUNTO DE ENTRADA Y CONTROL DE EJECUCIÓN DEL SCRIPT
# Objetivo: Avanzar el flujo y responder con el código de salida adecuado.
# =========================================================================

if __name__ == "__main__":
    # Ejecutar función principal
    execution_result = sql_correlated_subquery()

    # Validar resultado de ejecución
    if (
        isinstance(execution_result, bool)
        and not execution_result
    ):
        sys.exit(1)
    else:
        logging.info("✅ Proceso finalizado exitosamente")
        print("\n")
        sys.exit(0)