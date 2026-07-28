# =====================================================================
# Título: Pipeline de Extracción y Promedio Salarial por Departamento
#
# Objetivo: Consultar y extraer el promedio de ingresos mensuales desde
# SQL.
#
# Descripción: Conecta con una base de datos PostgreSQL, ejecuta una
# consulta con CTEs para calcular el salario medio por área y devuelve
# un DataFrame con los resultados listos para su análisis o consumo
# posterior.
#
# Archivo Python: day17_cte_department_salary_pipeline.py
#
# Archivo PNG: day17_cte_department_salary_pipeline.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos requeridos y ajustar las rutas del sistema
# =====================================================================

# Librería principal para manipulación y estructuración de los datos
import pandas as pd

# Módulo nativo del sistema para controlar la ejecución del script
import sys

# Módulo estándar para registrar eventos e incidencias durante la corrida
import logging

# Herramienta para gestionar rutas de archivos de forma independiente al SO
from pathlib import Path

# Calculamos la ruta raíz del proyecto navegando dos niveles hacia arriba
src_dir = str(Path(__file__).resolve().parents[1])

# Agregamos la ruta calculada al directorio de trabajo si no existe aún
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos la función interna para obtener una conexión SQL segura
from custom_functions.security_engine import get_secure_engine

# Importamos la función personalizada para inicializar el sistema de logs
from custom_functions.logging_pipeline import get_logging_pipeline

# Inicializamos el generador de registros de eventos para la sesión
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DEL PIPELINE
# Objetivo: Extraer y procesar la información salarial desde la BD
# =====================================================================


def execute_department_salary_pipeline():
    """Extrae datos procesados mediante CTEs múltiples desde PostgreSQL."""
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Establecemos el motor de conexión segura hacia la base de datos
        engine = get_secure_engine()

        # Definimos la sentencia SQL con la tabla temporal (CTE)
        query = """
            WITH avg_department_income AS (
                SELECT
                    j.department,
                    AVG(f.monthly_income) AS avg_income
                FROM fact_employees AS f
                JOIN dim_jobs AS j
                    ON f.job_id = j.job_id
                GROUP BY
                    j.department
            )

            SELECT 
                department,
                ROUND(avg_income::NUMERIC, 2) AS promedio_salarial
            FROM avg_department_income;
        """

        logging.info("⚡ Ejecutando pipeline de CTEs en PostgreSQL...")

        # Ejecutamos la consulta SQL y almacenamos la tabla en un Dataframe
        df_result = pd.read_sql(query, con=engine)

        # Validamos si la consulta devolvió información antes de continuar
        if not df_result.empty:
            logging.info("🚀 ==== INICIANDO MIDSET CTEs ====")

            print("\n✅ Datos cargados exitosamente.")
            print("\n👀 Vista previa:")
            print(df_result.head())

            print("\n")
            return df_result

        else:
            # En caso de no encontrar datos registramos el evento y paramos
            logging.info("❌ No se encontraron registros en la tabla principal.")
            print("\n")
            return False

    except Exception as e:
        # Atrapamos cualquier falla de red o consulta interrumpiendo la app
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Iniciar el proceso de extracción al ejecutar el archivo
# =====================================================================

if __name__ == "__main__":
    # Llamamos a la función de extracción y guardamos la tabla de retorno
    df_salaries = execute_department_salary_pipeline()

    # Si la extracción falló o vino vacía detenemos la corrida general
    if isinstance(df_salaries, bool) or df_salaries.empty:
        sys.exit(1)
