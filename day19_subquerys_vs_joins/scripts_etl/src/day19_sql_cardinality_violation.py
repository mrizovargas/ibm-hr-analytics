# =========================================================================
# Título: Simulación de Error por Violación de Cardinalidad en SQL
#
# Objetivo: Demostrar la falla al comparar un valor escalar contra una
# subconsulta SQL que devuelve múltiples filas.
#
# Descripción: Conecta a PostgreSQL y ejecuta una consulta SQL donde se
# utiliza un operador de comparación '>' frente a una subconsulta sin
# agregación, provocando y capturando la excepción nativa.
#
# Archivo Python: day19_sql_cardinality_violation.py
#
# Archivo PNG: day19_sql_cardinality_violation.png
# =========================================================================

# =========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar herramientas y asegurar la ruta base del proyecto.
# =========================================================================

# Registro de eventos y logs
import logging

# Gestión de rutas de archivos
from pathlib import Path

# Control del sistema y script
import sys

# Manipulación de datos
import pandas as pd

# Texto SQL y manejo de excepciones de BD
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, ProgrammingError

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
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN Y CAPTURA DE EXCEPCIONES SQL
# Objetivo: Ejecutar la consulta errónea y validar el error nativo.
# =========================================================================


def cardinality_violation() -> bool:
    """Ejecuta una consulta con error de cardinalidad intencional en

    PostgreSQL y valida la captura de la excepción nativa.
    """
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    # Motor seguro de conexión
    engine = get_secure_engine()

    # Consulta SQL con fallo de cardinalidad intencional
    query_erronea = text("""
        -- Selección de atributos clave
        SELECT
            employee_number,
            monthly_income

        -- Tabla principal de empleados
        FROM
            fact_employees

        -- Filtro con error escalar frente a múltiples filas
        WHERE
            monthly_income > (

                -- Subconsulta multifila que rompe la comparación escalar
                SELECT monthly_income FROM fact_employees
                UNION ALL
                SELECT monthly_income FROM fact_employees
            );
        """)

    # Estado de captura de excepción
    excepcion_capturada = False

    try:
        # Ejecutar instrucción SQL en la base de datos
        with engine.connect() as conexion:
            conexion.execute(query_erronea)

    except (ProgrammingError, DBAPIError) as e:
        # Confirmar éxito al capturar excepción de PostgreSQL
        excepcion_capturada = True
        logging.error("❌ Excepción nativa de PostgreSQL capturada correctamente:")
        logging.error(f"Detalle técnico: {e.orig}")

    finally:
        # Liberar recursos del motor
        engine.dispose()
        logging.info("🔒 Motor de conexión liberado.")

    # Retornar validación de la prueba
    return excepcion_capturada


# =========================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Controlar la ejecución del programa cuando se corre directo.
# =========================================================================

if __name__ == "__main__":
    # Iniciar flujo principal
    exito_prueba = cardinality_violation()

    # Validar captura de excepción
    if isinstance(exito_prueba, bool) and not exito_prueba:
        logging.warning(
            "⚠️ La prueba falló: No se generó la excepción de cardinalidad " "esperada."
        )
        sys.exit(1)
    else:
        logging.info("✅ Simulación finalizada exitosamente.")
        print("\n")
        sys.exit(0)
