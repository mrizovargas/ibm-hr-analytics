# =====================================================================
# Título: Auditoría de Integridad Relacional del Modelo en Estrella
#
# Objetivo: Verificar que no existan registros huérfanos entre la tabla
# de hechos y la dimensión de puestos en PostgreSQL.
#
# Descripción: Extrae las tablas fact_employees y dim_jobs, valida la
# coincidencia de sus llaves sustitutas y emite una alerta si detecta
# inconsistencias.
#
# Archivo Python: day20_star_schema_audit.py
#
# Archivo PNG: day20_star_schema_audit.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar módulos necesarios y ajustar rutas del proyecto.
# =====================================================================

import pandas as pd  # Procesamiento y análisis de datos en DataFrames
import sys  # Manejo del sistema operativo y rutas del intérprete
import logging  # Gestión de bitácoras y mensajes de estado del sistema
from pathlib import Path  # Manejo de rutas relativas y absolutas de archivos
from sqlalchemy import text  # Ejecución segura de sintaxis y consultas SQL

# Incorpora el directorio principal al sistema para importar módulos
source_path = str(Path(__file__).resolve().parents[1])  # Ruta del proyecto
if source_path not in sys.path:
    sys.path.insert(0, source_path)  # Añade la ruta a las dependencias

# Importación de utilidades personalizadas para logs y conexiones
from custom_functions.logging_pipeline import get_logging_pipeline  # Logs
from custom_functions.security_engine import get_secure_engine  # Conexión

get_logging_pipeline()  # Inicializa el registro de eventos


# =====================================================================
# BLOQUE 2: FUNCIÓN PRINCIPAL DE AUDITORÍA
# Objetivo: Validar la integridad referencial y detectar registros huérfanos.
# =====================================================================


def star_schema_audit() -> bool:
    """Audita la integridad relacional del modelo estrella creado en PostgreSQL."""
    print("\n")  # Espaciado de consola
    logging.info("==== INICIANDO CONEXIÓN CON POSTGRESQL ====")  # Log inicial
    try:
        db_engine = get_secure_engine()  # Genera el motor de conexión

        # Consulta para extraer registros de la tabla de hechos
        fact_empl_query = text("""
            SELECT *
            FROM fact_employees;
        """)  # Consulta tabla de hechos

        # Consulta para extraer registros de la dimensión puestos
        dim_job_query = text("""
            SELECT *
            FROM dim_jobs;
        """)  # Consulta dimensión de puestos

        # Abre la conexión con la base de datos PostgreSQL
        with db_engine.connect() as db_conecction:  # Inicia sesión segura
            # Carga de datos de la tabla de hechos a DataFrame
            df_fact = pd.read_sql_query(fact_empl_query, con=db_conecction)  # Hechos

            # Carga de datos de la dimensión de puestos a DataFrame
            df_jobs = pd.read_sql_query(dim_job_query, con=db_conecction)  # Dimensión

            # Identifica llaves de hechos que no existen en la dimensión
            huerfanos = df_fact[
                ~df_fact["sk_job_id"].isin(df_jobs["sk_job_id"])
            ]  # Busca llaves sin coincidencia

            # Revisa que las tablas contengan información previa al análisis
            if not df_fact.empty and not df_jobs.empty:  # Evalúa contenido
                logging.info(
                    "==== INICANDO PROCESAMIENTO Y LOGICA INTEGRADA DE NEGOCIO ==="
                )  # Log de procesamiento
                print("\n✅ Datos cargados exitosamente.")  # Notificación
                print("\n===== RESULTADO SQL + SQLALCHEMY =====")  # Resumen
                print(
                    f"📊 Registros en la tabla de hechos (fact_employees): "
                    f"{len(df_fact)}"
                )  # Muestra el total de hechos
                print(
                    f"📂 Registros en la tabla de dimensión (dim_jobs): "
                    f"{len(df_jobs)}"
                )  # Muestra el total de dimensión

                # Lanza error e interrumpe si encuentra registros huérfanos
                assert len(huerfanos) == 0, (
                    f"❌ ALERTA: Se encontraron {len(huerfanos)} " f"claves huérfanas."
                )  # Asertividad de control

                print(
                    "✅ PRUEBA EXITOSA: Integridad referencial del "
                    "modelo en estrella verificada al 100%."
                )  # Confirmación exitosa
                print("\n")  # Salto de línea
                db_engine.dispose()  # Cierra la conexión activada
                return True  # Devuelve estatus satisfactorio
            else:
                logging.info("❌ No se encontraron registros en la(s) tabla(s).")  # Log
                print("\n")  # Espacio en blanco
                return False  # Cancela flujo por falta de datos

    except Exception as e:
        logging.error(f"❌ Error detectado en: {e}")  # Registra la falla
        print("\n")  # Limpieza de consola
        sys.exit(1)  # Termina el programa con código de error


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y CONTROL DE EJECUCIÓN
# Objetivo: Ejecutar la auditoría e interrumpe el proceso si falla.
# =====================================================================

if __name__ == "__main__":
    execution_result = star_schema_audit()  # Inicia el pipeline

    # Evalúa si el resultado final devolvió un fallo o estado falso
    if isinstance(execution_result, bool) and not execution_result:  # Valida respuesta
        sys.exit(1)  # Aborta ejecución general del proceso
