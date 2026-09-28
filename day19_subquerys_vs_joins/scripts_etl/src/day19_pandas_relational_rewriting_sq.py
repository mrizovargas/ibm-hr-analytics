# =====================================================================
# Título: Evaluación de Rendimiento en Combinación de Datos (JOIN vs
# Subconsulta)
#
# Objetivo: Comparar la velocidad y consumo entre un filtrado básico y
# un JOIN.
#
# Descripción: Conecta a la base de datos, extrae empleados y puestos,
# aplica dos métodos de filtrado y mide cuál resulta más eficiente.
#
# Archivo Python: day19_pandas_relational_rewriting_sq.py
#
# Archivo PNG: day19_pandas_relational_rewriting_sq.png
# =====================================================================


# =====================================================================
# BLOQUE 1: Importación de librerías y módulos del sistema
# Objetivo: Cargar herramientas clave para manejar datos y archivos
# =====================================================================

# Registra eventos del sistema
import logging

# Maneja rutas de archivos
from pathlib import Path

# Controla la ejecución del sistema
import sys

# Mide tiempos de ejecución
import time

# Manipula y analiza datos
import pandas as pd

# Agregamos la carpeta principal al sistema para encontrar funciones
src_dir = str(Path(__file__).resolve().parents[1])
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos utilidades personalizadas de conexión y registro de eventos
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Iniciamos el sistema de logs para registrar lo que sucede en el proceso
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: Definición de la función principal de análisis
# Objetivo: Conectar a PostgreSQL y comparar las dos estrategias
# =====================================================================
def evaluate_merge_performance() -> bool:
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    # Creamos el motor seguro para la base de datos
    engine = get_secure_engine()

    try:
        # Abrimos la conexión activa
        with engine.connect() as conn:

            # Leemos la tabla de empleados y la tabla de puestos
            fact_employees = pd.read_sql_table("fact_employees", conn)
            dim_jobs = pd.read_sql_table("dim_jobs", conn)

            # Validamos que ninguna tabla esté vacía
            if not (fact_employees.empty or dim_jobs.empty):
                logging.info(
                    "🚀 ==== INICIANDO PROCESAMEINTO DE DATOS Y LÓGICA DE"
                    " NEGOCIO ===="
                )
                print("\n✅ Carga de datos exitosa.")

                # =====================================================
                # BLOQUE 3: Método 1 - Filtrado por lista (Subconsulta)
                # Objetivo: Probar el método tradicional de búsqueda (.isin)
                # =====================================================
                inefficient_start_time = time.perf_counter()

                # Buscamos IDs de puestos del área de ventas
                jobs_sales = dim_jobs[dim_jobs["department"] == "Sales"]["job_id"]

                # Filtramos empleados que coincidan con esos puestos
                inefficient_df = fact_employees[
                    fact_employees["job_id"].isin(jobs_sales)
                ][["employee_number", "job_id", "monthly_income"]]

                # Contamos los registros obtenidos
                total_records = len(inefficient_df)

                # Calculamos el tiempo total de este método
                inefficient_time = time.perf_counter() - inefficient_start_time

                # Mostramos los resultados en consola
                print(
                    "==== RESULTADO EQUIVALENTE A SUBCONSULTA (WHERE IN) EN"
                    " PANDAS ===="
                )
                print(f"\n📊 Total de registros encontrados: {total_records}")
                print("👀 Vista Previa:")
                print(inefficient_df.head().to_string(index=False))
                print("\n")

                # =====================================================
                # BLOQUE 4: Método 2 - Combinación directa (INNER JOIN)
                # Objetivo: Probar la fusión eficiente de tablas (pd.merge)
                # =====================================================
                optimized_start_time = time.perf_counter()

                # Unimos ambas tablas mediante la clave común 'job_id'
                merge_df = pd.merge(fact_employees, dim_jobs, on="job_id", how="inner")

                # Filtramos las columnas de interés para el departamento Ventas
                optimized_df = merge_df[merge_df["department"] == "Sales"][
                    [
                        "employee_number",
                        "department",
                        "job_role",
                        "monthly_income",
                    ]
                ]

                # Calculamos el tiempo gastado por la fusión
                optimized_time = time.perf_counter() - optimized_start_time

                total_records = len(optimized_df)

                # Mostramos los resultados del método optimizado
                print(
                    "==== RESULTADO EQUIVALENTE A INNER JOIN OPTIMIZADO EN"
                    " PANDAS ===="
                )
                print(f"\n📊 Total de registros encontrados: {total_records}")
                print("👀 Vista Previa:")
                print(optimized_df.head().to_string(index=False))
                print("\n")

                # =====================================================
                # BLOQUE 5: Evaluación de rendimiento e impacto
                # Objetivo: Comparar tiempos y uso de memoria entre métodos
                # =====================================================
                print(
                    "==== EVALUACIÓN DE RENDIMIENTO Y PERFILADO DE MEMORIA EN"
                    " PYTHON ===="
                )
                print(
                    "Tiempo Ejecución Estrategia Subconsulta (.isin):"
                    f" {inefficient_time * 1000:.4f} ms."
                )
                print(
                    "Tiempo Ejecución Estrategia JOIN (pd.merge):"
                    f" {optimized_time * 1000:.4f} ms."
                )

                print("\n")
                return True

            else:
                # Avisamos si no se encontraron datos suficientes
                print("\n")
                logging.warning("⚠️ No se encontraron registros en las tablas.")
                return False

    except Exception as e:
        # Capturamos cualquier falla y la registramos
        error_message = getattr(e, "orig", e)
        logging.error(f"❌ Error detectado en:\n{error_message}")
        print("\n")
        sys.exit(1)
    finally:
        # Cerramos la conexión para liberar memoria del sistema
        engine.dispose()
        logging.info("🔒 Motor de conexión liberado.")


# =====================================================================
# BLOQUE 6: Punto de entrada del programa
# Objetivo: Iniciar la ejecución e informar el estado final
# =====================================================================
if __name__ == "__main__":
    execution_result = evaluate_merge_performance()

    # Evaluamos si la ejecución fue exitosa o no
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)
    else:
        logging.info("✅ Proceso finalizado exitosamente.")
        print("\n")
        sys.exit(0)
