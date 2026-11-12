# =====================================================================
# Título: Auditoría de Valores Nulos en Claves de Empleados
#
# Objetivo: Verificar la ausencia de valores nulos en columnas clave de
# la tabla de empleados para asegurar la integridad referencial.
#
# Descripción: El script conecta a PostgreSQL, extrae todos los registros
# de la tabla de empleados, calcula los nulos totales y valida con
# aserciones que las llaves principales y foráneas estén completas.
#
# Archivo Python: day22_employee_nulls_audit_isnull_meth.py
#
# Archivo PNG: day22_employee_nulls_audit_isnull_meth.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y configurar la ruta base.
# =====================================================================

# Librería para análisis y manipulación de datos
import pandas as pd

# Módulo para interactuar con el sistema operativo
import sys

# Módulo para registrar eventos e incidencias de ejecución
import logging

# Utilidad para gestionar rutas de archivos de forma limpia
from pathlib import Path

# Función para definir consultas SQL de forma segura
from sqlalchemy import text

# Obtenemos la ruta del directorio principal del proyecto
source_path = str(Path(__file__).resolve().parents[1])

# Agregamos la ruta base al sistema para permitir importaciones
if source_path not in sys.path:
    sys.path.insert(0, source_path)

# Importamos funciones personalizadas de registro y seguridad
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Inicializamos el sistema de registros
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE AUDITORÍA
# Objetivo: Conectar a la base de datos y validar valores nulos.
# =====================================================================


def nulls_absence() -> bool:
    """Valida la ausencia de nulos en llaves de la tabla de empleados."""

    # Imprimimos un salto de línea para ordenar la consola
    print("\n")

    # Registramos el inicio de la conexión con la base de datos
    logging.info("🚀 ==== INICANDO CONEXIÓN CON POSTGRESQL====")

    try:
        # Creamos el motor de conexión segura
        db_engine = get_secure_engine()

        # Definimos la consulta SQL con comentarios explicativos
        sql_query = text("""
            SELECT
                -- Seleccionamos todas las columnas de la tabla
                *
            FROM
                -- Tabla principal que almacena los registros de empleados
                fact_employees;
        """)

        # Abrimos la conexión de forma segura con la base de datos
        with db_engine.connect() as db_connection:
            # Ejecutamos la consulta y cargamos los datos en un DataFrame
            df_result = pd.read_sql_query(sql_query, con=db_engine)

        # Validamos si la consulta devolvió registros
        if not df_result.empty:
            # Registramos el inicio de la lógica de negocio y procesamiento
            logging.info(
                "⚡ ==== INICIANDO PROCESAMIENTO DE DATOS Y LÓGICA "
                "INTREGRADA DE NEGOCIO ===="
            )

            # Informamos el éxito de la carga de datos
            print("\n✅ Datos cargados exitosamente.")
            print("\n==== RESULTADO SQL + SQLALCHEMY ====")

            # Calculamos la cantidad de valores nulos por columna
            total_nulls = df_result.isnull().sum()
            print("\n==== REPORTE DE VALORES NULOS ====")

            # Mostramos el conteo total de nulos encontrados
            print(f"Total de valores nulos:\n{total_nulls}")

            # Validamos que la llave primaria del empleado no tenga nulos
            assert (
                df_result["sk_employee_id"].isnull().sum() == 0
            ), "❌ Error: la llave primaria 'sk_employee_id' contiene valores nulos."

            # Validamos que la llave foránea del puesto no contenga nulos
            assert (
                df_result["sk_job_id"].isnull().sum() == 0
            ), "❌ Error: La llave foránea 'sk_job_id' contiene valores nulos."

            # Validamos que la llave foránea demográfica esté completa
            assert (
                df_result["sk_demographics_id"].isnull().sum() == 0
            ), "❌ Error: la llave foránea 'sk_demographics_id' contiene valores nulos."

            print("\n")

            # Cerramos y liberamos el motor de base de datos
            db_engine.dispose()

            # Retornamos True indicando que la auditoría pasó con éxito
            return True
        else:
            # Registramos si no se encontraron registros en la tabla
            logging.info("❌ No se encontraron registros en la tabla.")
            print("\n")

            # Retornamos False por falta de datos
            return False

    except Exception as e:
        # Capturamos cualquier excepción y registramos el error
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")

        # Finalizamos el programa con código de error
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Controlar la ejecución directa del script en Python.
# =====================================================================

# Verificamos si el archivo se está ejecutando directamente
if __name__ == "__main__":

    # Ejecutamos la función principal y almacenamos el resultado
    execution_result = nulls_absence()

    # Validamos si ocurrió un fallo lógico para detener la ejecución
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)
