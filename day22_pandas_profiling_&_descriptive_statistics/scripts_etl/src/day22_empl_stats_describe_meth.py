# =====================================================================
# Título: Extracción de Datos de Empleados y Análisis Estadístico Básico
#
# Objetivo: Conectar a PostgreSQL, extraer métricas de empleados y generar
# un resumen estadístico descriptivo de los datos obtenidos.
#
# Descripción: El script configura el entorno de trabajo, establece una
# conexión segura con la base de datos, ejecuta una consulta SQL sobre la
# tabla de empleados y calcula estadísticas básicas usando Pandas.
#
# Archivo Python: day22_empl_stats_describe_meth.py
#
# Archivo PNG: day22_empl_stats_describe_meth.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar módulos necesarios y agregar la ruta base del proyecto.
# =====================================================================

# Librería para manipulación y análisis de datos
import pandas as pd

# Configurar el formato visual para que muestre siempre 2 decimales en flotantes
pd.options.display.float_format = "{:.2f}".format

# Módulo para interactuar con el sistema operativo
import sys

# Módulo para registrar eventos e incidencias durante la ejecución
import logging

# Herramienta para gestionar rutas de archivos de forma limpia
from pathlib import Path

# Función para convertir texto en una consulta SQL segura
from sqlalchemy import text

# Calculamos la ruta del directorio principal de nuestro proyecto
source_path = str(Path(__file__).resolve().parents[1])

# Agregamos la ruta base al sistema para importar módulos propios
if source_path not in sys.path:
    sys.path.insert(0, source_path)

# Funciones personalizadas para el registro de logs y conexión segura
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Inicializamos el sistema personalizado de registro de mensajes
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# Objetivo: Consultar la base de datos y calcular estadísticas clave.
# =====================================================================


def describe_method() -> bool:
    """Extrae datos de PostgreSQL y genera un resumen estadístico."""

    # Imprimimos una línea en blanco para ordenar la salida
    print("\n")

    # Registramos en el log que iniciamos la conexión a la base de datos
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Creamos el motor de conexión segura
        db_engine = get_secure_engine()

        # Definimos la consulta SQL para obtener columnas clave de empleados
        sql_query = text("""
            SELECT
                -- Obtenemos el ingreso mensual desde la tabla de hechos
                f.monthly_income,
                -- Obtenemos la edad desde el catálogo maestro
                e.age,
                -- Obtenemos los años en la empresa desde la tabla de hechos
                f.years_at_company
            FROM
                -- Tabla principal con métricas numéricas del empleado
                fact_employees AS f
            INNER JOIN
                -- Tabla complementaria con datos demográficos del empleado
                employee_master_data AS e
                -- Cruzamos ambas tablas usando el número único de empleado
                ON f.employee_number = e.employee_number;
        """)

        # Abrimos la conexión con la base de datos de manera segura
        with db_engine.connect() as db_connection:
            # Ejecutamos la consulta y guardamos el resultado en una tabla
            df_result = pd.read_sql_query(sql_query, con=db_engine)

        # Verificamos si obtuvimos registros en la consulta
        if not df_result.empty:
            # Registramos el inicio del procesamiento de datos
            logging.info(
                "⚡ ==== INICIANDO PROCESAMIENTO Y LÓGICA " "INTEGRADA DE NEGOCIO ===="
            )

            # Notificamos que los datos se cargaron con éxito
            print("\n✅ Datos cargados exitosamente")
            print("\n ==== RESULTADO SQL + SQLALCHEMY ====")

            # Generamos estadísticas descriptivas (promedios, máximos, etc.)
            resumen_estadistico = df_result.describe()

            # Mostramos la tabla con el resumen estadístico
            print(resumen_estadistico)
            print("\n")

            # Liberamos los recursos del motor de base de datos
            db_engine.dispose()

            # Indicamos que el proceso terminó correctamente
            return True
        else:
            # Informamos en el log si la tabla no contenía información
            logging.info("❌ No se encontraron registros en la tabla.")
            print("\n")

            # Retornamos falso indicando ausencia de datos
            return False

    except Exception as es:
        # Capturamos cualquier falla e informamos en el registro de errores
        logging.error(f"❌ Error detectado en: {es}")
        print("\n")

        # Detenemos la ejecución del programa con código de error
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Controlar la ejecución automática al llamar el archivo.
# =====================================================================

# Comprobamos si el archivo se está ejecutando directamente
if __name__ == "__main__":

    # Ejecutamos la función principal y guardamos el resultado
    excecution_result = describe_method()

    # Si la ejecución devuelve False o algo distinto a True, detenemos
    if isinstance(excecution_result, bool) and not excecution_result:
        sys.exit(1)
