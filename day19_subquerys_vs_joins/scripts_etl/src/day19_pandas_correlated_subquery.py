# =====================================================================
# Título: Filtro de Empleados en Puestos de Alto Riesgo de Rotación
#
# Objetivo: Identificar empleados asociados a puestos con alto riesgo
# de rotación combinando tablas de hechos y dimensiones en Pandas.
#
# Descripción: Conecta a PostgreSQL para extraer las tablas de
# empleados y puestos. Aplica una lógica equivalente a un WHERE EXISTS
# en SQL seguida de un INNER JOIN para recuperar atributos dimensionales
# y generar el reporte final.
#
# Archivo Python: day19_pandas_correlated_subquery.py
#
# Archivo PNG: day19_pandas_correlated_subquery.png
# =====================================================================


# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y configurar las rutas del
# proyecto para acceder a funciones personalizadas.
# =====================================================================

# Manipulación de datos
import pandas as pd

# Control del sistema y terminación del script
import sys

# Registro de logs
import logging

# Gestión multiplataforma de rutas
from pathlib import Path

# Calcular e incluir la ruta raíz del proyecto en sys.path
src_dir = str(Path(__file__).resolve().parents[1])

if src_dir not in sys.path:
    sys.path.append(src_dir)

# Importar motor de conexión PostgreSQL
from custom_functions.security_engine import get_secure_engine

# Importar e inicializar el sistema de logs
from custom_functions.logging_pipeline import get_logging_pipeline

get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DEL PIPELINE
# Objetivo: Definir la secuencia de conexión, extracción, filtrado
# y despliegue de datos de empleados.
# =====================================================================


def pandas_correlated_subquery() -> bool:
    # Salto de línea para formato en consola
    print("\n")

    # Log de inicio de conexión
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ===")

    # Crear motor de conexión seguro
    engine = get_secure_engine()

    try:
        # Abrir conexión
        with engine.connect() as conexion:

            # =========================================================
            # BLOQUE 3: EXTRACCIÓN Y CARGA DE TABLAS DESDE POSTGRESQL
            # Objetivo: Leer las tablas de empleados y puestos desde la
            # base de datos y cargarlas como DataFrames en memoria.
            # =========================================================

            # Cargar tablas de hechos y dimensiones
            fact_employees = pd.read_sql_table("fact_employees", con=conexion)

            dim_jobs = pd.read_sql_table("dim_jobs", con=conexion)

            # Validar que existan datos en ambas tablas
            if not (fact_employees.empty or dim_jobs.empty):
                logging.info(
                    "🚀 ==== INICIANDO PROCESAMIENTO DE DATOS Y "
                    "LÓGICA DE NEGOCIO ===="
                )
                print("\n✅ Carga de datos exitosa.")

                # =====================================================
                # BLOQUE 4: PROCESAMIENTO Y FILTRADO DE DATOS (PANDAS)
                # Objetivo: Identificar puestos de alto riesgo y filtrar
                # a los empleados asociados de manera vectorizada.
                # =====================================================

                # Filtrar puestos con alto riesgo de rotación
                puestos_alto_riesgo = dim_jobs[dim_jobs["high_turnover_risk"] == "Yes"]

                # Filtrar empleados según puestos seleccionados (equivale a WHERE EXISTS)
                df_alto_riesgo_pandas = fact_employees[
                    fact_employees["job_id"].isin(puestos_alto_riesgo["job_id"])
                ]

                # Cruzar empleados con datos del puesto (INNER JOIN)
                df_merge_alto_riesgo = pd.merge(
                    left=puestos_alto_riesgo,
                    right=df_alto_riesgo_pandas,
                    on="job_id",
                    how="inner",
                )

                # Seleccionar columnas necesarias para el reporte
                columnas_deseadas = [
                    "employee_number",
                    "department",
                    "job_role",
                    "monthly_income",
                ]
                df_resultado_final = df_merge_alto_riesgo[columnas_deseadas]

                # Contar total de registros filtrados
                total_filas = len(df_resultado_final)

                # =====================================================
                # BLOQUE 5: DESPLIEGUE DE RESULTADOS Y SALIDA
                # Objetivo: Mostrar en consola el resumen y la vista
                # previa de los datos procesados exitosamente.
                # =====================================================

                print(
                    "\n==== RESULTADO PANDAS (Procesamiento "
                    "Vectorizado + Conexión SQLAlchemy) ===="
                )
                print(f"\n Total de registros encontrados: {total_filas}")
                print("\n👀 Vista previa:")
                print(df_resultado_final.head().to_string(index=False))
                print("\n")

                # Retornar True al completar exitosamente
                return True

            else:
                # Notificar si no hay datos disponibles
                print("\n")
                logging.warning("⚠️ No se encontraron registros en la tabla.")
                return False

    except Exception as e:
        # Registrar cualquier error e interrumpir script
        mensaje_error = getattr(e, "orig", e)
        logging.error(f"❌ Error detectado en:\n{mensaje_error}")
        print("\n")

        sys.exit(1)

    finally:
        # Liberar recursos de la conexión
        engine.dispose()
        logging.info("🔒 Motor de conexión liberado.")


# =====================================================================
# BLOQUE 6: PUNTO DE ENTRADA Y CONTROL DE EJECUCIÓN DEL SCRIPT
# Objetivo: Disparar la función principal y definir el código de salida
# del sistema operativo según el resultado del pipeline.
# =====================================================================

if __name__ == "__main__":
    # Ejecutar el pipeline
    df_pandas_correlated_subquery = pandas_correlated_subquery()

    # Manejar el código de salida según el resultado
    if (
        isinstance(df_pandas_correlated_subquery, bool)
        and not df_pandas_correlated_subquery
    ):
        sys.exit(1)

    else:
        logging.info("✅ Proceso finalizado exitosamente.")
        print("\n")
        sys.exit(0)
