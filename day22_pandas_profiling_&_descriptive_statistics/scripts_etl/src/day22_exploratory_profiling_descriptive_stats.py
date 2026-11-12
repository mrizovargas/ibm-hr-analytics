# =====================================================================
# Título: Perfilamiento Exploratorio y Estadística Descriptiva de
# Empleados
#
# Objetivo: Conectar a PostgreSQL, extraer los datos maestros de
# empleados y generar un reporte con información general, estadísticas
# y nulos.
#
# Descripción: El script conecta de forma segura a la base de datos,
# extrae todos los registros de la tabla maestra, muestra un resumen
# descriptivo completo y audita la presencia de valores nulos por
# columna.
#
# Archivo Python: day22_exploratory_profiling_descriptive_stats.py
#
# Archivo PNG: day22_exploratory_profiling_descriptive_stats.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y configurar la ruta base.
# =====================================================================

# Librería para análisis y manipulación de datos
import pandas as pd

# Configuramos el formato predeterminado para mostrar dos decimales
pd.options.display.float_format = "{:.2f}".format

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
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE PERFILAMIENTO
# Objetivo: Consultar datos y generar reportes estadísticos y de nulos.
# =====================================================================


def expl_prof_desc_stats() -> bool:
    """Extrae datos de PostgreSQL y genera un perfilamiento exploratorio."""

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
                -- Seleccionamos todas las columnas disponibles en la tabla
                *
            FROM
                -- Tabla maestra que almacena los registros de empleados
                fact_employees;
        """)

        # Abrimos la conexión de forma segura con la base de datos
        with db_engine.connect() as db_connection:
            # Ejecutamos la consulta y cargamos los datos en un DataFrame
            df_result = pd.read_sql_query(sql_query, con=db_connection)

        # Validamos si la consulta devolvió registros
        if not df_result.empty:
            # Registramos el inicio de la lógica de negocio y procesamiento
            logging.info(
                "⚡ ==== INCIANDO PROCESAMIENTO Y LÓGICA " "INTERNA DE NEGOCIO ===="
            )

            # Informamos el éxito de la carga de datos
            print("\n✅ Datos cargados exitosamente.")
            print("\n ==== RESULTADO SQL + SQLALCHEMY ====")
            print("\n ==== INFORMACIÓN GENERAL DEL DATAFRAME ====")

            # Mostramos la estructura general y tipos de datos del DataFrame
            print(df_result.info())

            print("\n📈 ==== RESÚMEN ESTADÍSTICO DESCRIPTIVO ====")

            # Resumimos columnas numéricas y categóricas (texto)
            print(df_result.describe(include="all"))

            print("\n ==== AUDITORÍA DE VALORES NULOS POR COLUMNA ====")

            # Mostramos el conteo de valores nulos encontrados por columna
            print(df_result.isnull().sum())
            print("\n")

            # Cerramos y liberamos el motor de base de datos
            db_engine.dispose()

            # Retornamos True indicando ejecución exitosa
            return True
        else:
            # Registramos si no se encontraron registros en la tabla
            logging.info("❌ No se encontraron regisros en la tabla")
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
    execution_result = expl_prof_desc_stats()

    # Validamos si ocurrió un fallo lógico para detener la ejecución
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)
