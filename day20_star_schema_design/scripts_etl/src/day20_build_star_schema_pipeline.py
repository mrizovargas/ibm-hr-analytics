# =====================================================================
# Título: Pipeline de Carga de Modelo en Estrella en PostgreSQL
#
# Objetivo: Extraer datos maestros de empleados, crear las dimensiones
# de puestos y demografía, e insertarlas en tablas de prueba.
#
# Descripción: Conecta a la base de datos PostgreSQL, lee la información
# de empleados en un DataFrame, transforma y elimina duplicados de las
# tablas dimensionales, y guarda los datos transformados.
#
# Archivo Python: day20_build_star_schema_pipeline.py
#
# Archivo PNG: day20_build_star_schema_pipeline.png
# =====================================================================

"""
Módulo de construcción e inserción del Modelo en Estrella en PostgreSQL.
Adhiere a las directrices de estilo PEP 8.
"""

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar dependencias y ajustar las rutas del sistema.
# =====================================================================

import pandas as pd  # Manejo e ingeniería de datos en DataFrames
import sys  # Control del sistema y rutas de Python
import logging  # Registro de eventos y logs del proceso
from pathlib import Path  # Gestión de rutas del sistema de archivos
from sqlalchemy import text  # Ejecución de consultas SQL seguras

# Agrega la ruta raíz del proyecto para importar módulos propios
source_path = str(Path(__file__).resolve().parents[1])
if source_path not in sys.path:
    sys.path.insert(0, source_path)

# Importa funciones personalizadas del proyecto
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

get_logging_pipeline()  # Inicializa la configuración de logs


# =====================================================================
# BLOQUE 2: FUNCIÓN PRINCIPAL DEL PIPELINE
# Objetivo: Extraer, transformar y cargar el modelo en estrella.
# =====================================================================


def build_star_schema_pipeline() -> bool:
    """Extrae el dataset plano, normaliza dimensiones y carga el modelo en estrella."""
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Obtiene el motor de base de datos seguro
        db_engine = get_secure_engine()

        # Consulta SQL para extraer los datos maestros de empleados
        sql_query = text("""
            SELECT *                           -- Consulta todos los campos
            FROM employee_master_data;        -- Desde la tabla maestra
        """)

        # Abre conexión con la base de datos
        with db_engine.connect() as db_connection:
            # Carga la consulta SQL en un DataFrame de pandas
            df_processed = pd.read_sql_query(sql_query, con=db_connection)

            if not df_processed.empty:
                logging.info("⚡ ==== CARGANDO DATOS PROCESADOS DESDE POSTGRESQL ====")

                # -------------------------------------------------------------
                # Carga de Dimensión Puestos (dim_jobs)
                # -------------------------------------------------------------
                # Filtra columnas de puestos, remueve duplicados y reinicia índice
                df_jobs = (
                    df_processed[["job_role", "department", "standard_hours"]]
                    .drop_duplicates()
                    .reset_index(drop=True)
                )

                # Inserta los datos en la tabla de dimensión de puestos
                df_jobs.to_sql(
                    "dim_jobs", con=db_connection, if_exists="append", index=False
                )
                print("\n✅ Dimensión 'dim_jobs' cargada exitosamente.")

                # -------------------------------------------------------------
                # Carga de Dimensión Demográfica (dim_demographics)
                # -------------------------------------------------------------
                # Filtra datos demográficos, elimina duplicados y reinicia índice
                df_demo = (
                    df_processed[["gender", "education_field", "marital_status"]]
                    .drop_duplicates()
                    .reset_index(drop=True)
                )

                # Inserta los datos en la tabla demográfica de prueba
                df_demo.to_sql(
                    "dim_demographics",
                    con=db_connection,
                    if_exists="append",
                    index=False,
                )
                print("✅ Dimensión 'dim_demographics' cargada exitosamente.")

                # -------------------------------------------------------------
                # CONFIRMAR TRANSACCIÓN EN POSTGRESQL (Evita ROLLBACK implícito)
                # -------------------------------------------------------------
                db_connection.commit()
                print("\n")

                db_engine.dispose()  # Cierra las conexiones activas del motor
                return True

            else:
                logging.info("❌ No se encontraron registros en la tabla.")
                print("\n")
                return False

    except Exception as e:
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA DEL SCRIPT
# Objetivo: Controlar la ejecución directa y gestionar fallos.
# =====================================================================

if __name__ == "__main__":
    excecution_result = build_star_schema_pipeline()  # Ejecuta pipeline

    # Valida si la ejecución falló para finalizar el sistema con error
    if isinstance(excecution_result, bool) and not excecution_result:
        sys.exit(1)
