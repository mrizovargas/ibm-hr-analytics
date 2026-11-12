# =====================================================================
# Título: Perfil Estadístico y Análisis de Datos de Empleados
#
# Objetivo: Conectar a PostgreSQL, extraer información clave de
# empleados y generar un perfil estadístico descriptivo completo.
#
# Descripción: El script configura el entorno, establece una conexión
# segura con la base de datos, extrae datos demográficos y salariales,
# y calcula métricas como la media, mediana, moda y desviación estándar.
#
# Archivo Python: day22_empl_stats_profiling.py
#
# Archivo PNG: day22_empl_stats_profiling.png
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
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE PERFIL ESTADÍSTICO
# Objetivo: Consultar la base de datos y calcular métricas estadísticas.
# =====================================================================


def stadistic_profiling() -> bool:
    """Extrae datos de PostgreSQL y genera un perfil estadístico."""

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
                -- Identificador único del empleado
                employee_id,
                -- Edad actual del colaborador
                age,
                -- Departamento al que pertenece el empleado
                department,
                -- Ingreso monetario mensual recibido
                monthly_income,
                -- Años acumulados de permanencia en la empresa
                years_at_company
            FROM
                -- Tabla maestra que almacena la información de los empleados
                employee_master_data;
        """)

        # Abrimos la conexión de forma segura con la base de datos
        with db_engine.connect() as db_connection:
            # Ejecutamos la consulta y cargamos los datos en un DataFrame
            df_employees = pd.read_sql_query(sql_query, con=db_connection)

        # Validamos si la consulta devolvió registros
        if not df_employees.empty:
            # Registramos el inicio de la lógica de negocio y procesamiento
            logging.info(
                "⚡ ==== INICIANDO PROCESAMIENTO Y LÓGICA " "INTEGRADA DE NEGOCIO ===="
            )

            # Informamos el éxito de la carga de datos
            print("\n ✅ Datos cargados exitosamente.")
            print("\n==== RESULTADO SQL + SQLALCHEMY ====")
            print("==== 📈 1. RESUMEN ESTADÍSTICO DESCRIPTIVO (Pandas) ====")

            # Generamos un resumen estadístico para edad, ingresos y antigüedad
            print(
                df_employees[["age", "monthly_income", "years_at_company"]].describe().T
            )

            print("\n==== 📊 2. TENDENCIAS CENTRALES ADICIONALES ====")

            # Calculamos y mostramos la mediana de los ingresos mensuales
            print(
                "Mediana de Ingresos Mensuales: "
                f"{df_employees['monthly_income'].median():.2f}"
            )

            # Calculamos y mostramos la moda de los años en la empresa
            print(
                "Moda de Años en la Empresa: "
                f"{df_employees['years_at_company'].mode()[0]}"
            )

            # Calculamos y mostramos la desviación estándar de los ingresos
            print(
                "Desviación Estándar de Ingresos: "
                f"{df_employees['monthly_income'].std():.2f}"
            )
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
    execution_result = stadistic_profiling()

    # Validamos si ocurrió un fallo lógico para detener la ejecución
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)
