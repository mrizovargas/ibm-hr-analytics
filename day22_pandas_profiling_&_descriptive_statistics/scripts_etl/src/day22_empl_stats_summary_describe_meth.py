# =====================================================================
# Título: Resumen Estadístico y Auditoría de Rangos en Empleados
#
# Objetivo: Conectar a PostgreSQL, extraer métricas clave de la tabla
# de empleados y validar la coherencia estadística de los datos.
#
# Descripción: El script conecta a la base de datos de manera segura,
# extrae los registros de empleados, genera estadísticas descriptivas y
# valida que los valores mínimos sean mayores a cero.
#
# Archivo Python: day22_empl_stats_summary_describe_meth.py
#
# Archivo PNG: day22_empl_stats_summary_describe_meth.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y configurar la ruta base.
# =====================================================================

# Librería para análisis y manipulación de datos
import pandas as pd

# Configurar el formato visual para que muestre siempre 2 decimales en flotantes
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
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE ESTADÍSTICAS
# Objetivo: Consultar datos y generar estadísticas descriptivas.
# =====================================================================


def stadistics_summary() -> bool:
    """Extrae datos de PostgreSQL y genera un resumen estadístico."""

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
                -- Tabla principal que almacena los registros de empleados
                employee_master_data;
        """)

        # Abrimos la conexión de forma segura con la base de datos
        with db_engine.connect() as db_connection:
            # Ejecutamos la consulta y cargamos los datos en un DataFrame
            df_result = pd.read_sql_query(sql_query, con=db_engine)

        # Validamos si la consulta devolvió registros
        if not df_result.empty:
            # Registramos el inicio de la lógica de negocio
            logging.info(
                "⚡ ==== INICIANDO PROCESAMIENTO Y LÓGICA " "INTEGRADA DE NEGOCIO ===="
            )

            # Informamos el éxito de la carga de datos
            print("\n✅ Datos cargados exitosamente.")
            print("\n ==== RESULTADO SQL + SQLALCHEMY ====")

            # Extraemos estadísticas descriptivas de ingresos y edad
            stadistic_summary = df_result[["monthly_income", "age"]].describe()

            print("📈 ==== ESTADÍSTICAS DESCRIPTIVAS ====")

            # Mostramos las métricas de mínimo, máximo y promedio
            print(stadistic_summary.loc[["min", "max", "mean"]])

            # Obtenemos el ingreso mínimo para validar rangos
            min_income = df_result["monthly_income"].min()

            # Obtenemos la edad mínima para validar rangos
            min_age = df_result["age"].min()

            # Verificamos que no existan valores menores o iguales a cero
            if min_income <= 0 or min_age <= 0:
                raise ValueError(
                    "❌ ¡Alerta! Se encontraron variables menores o "
                    "iguales a cero en variables estrictamente positivas."
                )
            else:
                # Informamos que la validación estadística fue exitosa
                print("\n✅ Verificación de coherencia estadística superada con éxito.")

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
    execution_result = stadistics_summary()

    # Validamos si ocurrió un fallo lógico para detener la ejecución
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)
