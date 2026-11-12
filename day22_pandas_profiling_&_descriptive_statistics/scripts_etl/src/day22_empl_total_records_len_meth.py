# =====================================================================
# Título: Extracción y Conteo Total de Registros de Empleados
#
# Objetivo: Conectar a PostgreSQL, consultar la tabla de empleados y
# contar el número total de registros disponibles.
#
# Descripción: El script configura el entorno, abre una conexión segura
# a la base de datos, extrae todos los registros de empleados y calcula
# el total de filas almacenadas.
#
# Archivo Python: day22_employee_total_records_len_meth.py
#
# Archivo PNG: day22_employee_total_records_len_meth.png
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
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# Objetivo: Consultar la base de datos y contar el total de registros.
# =====================================================================


def total_records() -> bool:
    """Extrae datos de PostgreSQL y cuenta los registros totales."""

    # Imprimimos un salto de línea para ordenar la consola
    print("\n")

    # Registramos el inicio de la conexión con la base de datos
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Creamos el motor de conexión segura
        db_engine = get_secure_engine()

        # Definimos la consulta SQL con comentarios explicativos
        sql_query = text("""
            SELECT
                -- Seleccionamos todas las columnas disponibles
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
            # Registramos el inicio de la lógica de negocio
            logging.info(
                "⚡ ==== INICIANDO PROCESAMIENTO Y LÓGICA INTEGRADA DE NEGOCIO ===="
            )

            # Informamos el éxito de la carga de datos
            print("\n✅ Datos cargados exitosamente.")
            print("\n ==== RESULTADO SQL + SQLAlchemy ====")

            # Mostramos el total de los registros extraídos del DataFrame
            print(f"Total de registros (df_result): {len(df_result)}")
            print("\n")

            # Cerramos y liberamos el motor de base de datos
            db_engine.dispose()

            # Retornamos True indicando ejecución exitosa
            return True
        else:
            # Registramos si no se encontraron registros en la tabla
            logging.info("❌ No se encontraron registros en la tabla.")
            print("\n")

            # Retornamos False por falta de datos
            return False

    except Exception as e:
        # Capturamos cualquier excepción y registramos el error
        logging.error(f"❌ Error detectado en: {e}.")
        print("\n")

        # Finalizamos el programa con código de error
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Controlar la ejecución directa del script de Python.
# =====================================================================

# Verificamos si el archivo se está ejecutando directamente
if __name__ == "__main__":

    # Ejecutamos la función principal y almacenamos el resultado
    excecution_result = total_records()

    # Validamos si ocurrió un fallo lógico para detener la ejecución
    if isinstance(excecution_result, bool) and not excecution_result:
        sys.exit(1)
