# =====================================================================
# Título: Evaluación Comparativa de Tiempos de Ejecución (Subconsulta
# vs JOIN)
#
# Objetivo: Medir y comparar la velocidad de respuesta entre una
# consulta SQL con subconsulta y una consulta con JOIN usando SQLAlchemy
# y Pandas.
#
# Descripción: Conecta a PostgreSQL, ejecuta dos consultas equivalentes
# para traer a los empleados del área de Ventas, toma el tiempo de cada
# una y muestra los resultados de rendimiento en consola.
#
# Archivo Python: day19_case_study_benchmark_subqry_vs_join.py
#
# Archivo PNG: day19_case_study_benchmark_subqry_vs_join.png
# =====================================================================


# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y ajustar las rutas del sistema.
# =====================================================================
# Manipulación de datos
import pandas as pd

# Control del sistema y script
import sys

# Registro de eventos y logs
import logging

# Registra  el tiempo de ejecución
import time

# Gestión de rutas de archivos
from pathlib import Path

# Ejecución de SQL plano en SQLAlchemy
from sqlalchemy import text

# Configura la ruta raíz para importar funciones personalizadas del proyecto
source_path = str(Path(__file__).resolve().parents[1])
if source_path not in sys.path:
    sys.path.insert(0, source_path)

from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Activa el sistema de registros para auditar la ejecución
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DEL PIPELINE Y EJECUCIÓN DE LA CONSULTA SQL
# Objetivo: Conectar a la base de datos, ejecutar la consulta y mostrar.
# =====================================================================


def benchmark_queries() -> bool:
    """Mide y compara la velocidad de respuesta entre Subconsultas y JOINS."""
    print("\n")
    logging.info("==== INICIANDO CONEXIÓN CON 🚪 POSTGRESQL ====")
    try:
        # Crea la conexión segura a la base de datos
        db_engine = get_secure_engine()

        # Consulta 1: Obtiene datos filtrando mediante una subconsulta
        query_subquery = text("""
            -- ====================================================================================
            -- BLOQUE 3.1: SELECCIÓN Y ORIGEN DE DATOS
            -- Objetivo: Elegir los datos clave de los empleados desde la tabla principal.
            -- ====================================================================================

            SELECT 
                employee_number, -- Número de identificación único de cada empleado
                monthly_income   -- Ingreso mensual registrado del empleado
            FROM 
                fact_employees   -- Tabla principal con la información de empleados

            -- ====================================================================================
            -- BLOQUE 4.1: FILTRADO POR SUBCONSULTA
            -- Objetivo: Restringir los resultados al departamento de Ventas.
            -- ====================================================================================

            WHERE 
                job_id IN (      -- Filtra puestos que pertenezcan al área seleccionada
                    SELECT 
                        job_id   -- Obtiene identificadores de puestos requeridos
                    FROM 
                        dim_jobs -- Catálogo general de puestos laborales
                    WHERE 
                        department = 'Sales' -- Selecciona solo el área de Ventas
                );
        """)

        # Consulta 2: Obtiene los mismos datos mediante una unión de tablas
        query_join = text("""
            -- ====================================================================================
            -- BLOQUE 3.2: SELECCIÓN DE CAMPOS
            -- Objetivo: Especificar las columnas requeridas de la tabla de empleados.
            -- ====================================================================================

            SELECT 
                f.employee_number, -- Identificador único del empleado
                f.monthly_income   -- Sueldo mensual percibido

            
            -- ====================================================================================
            -- BLOQUE 4.2: CRUCE Y FILTRADO DE TABLAS
            -- Objetivo: Combinar datos con el catálogo de puestos y filtrar por departamento.
            -- ====================================================================================

            FROM 
                fact_employees AS f -- Tabla principal de datos laborales
            INNER JOIN 
                dim_jobs AS j       -- Catálogo de cargos y áreas
                ON f.job_id = j.job_id -- Relación por la clave de puesto de trabajo
            WHERE 
                j.department = 'Sales'; -- Filtra para incluir únicamente a Ventas
        """)

        # Manejo explícito de conexiones dentro del pool de SQLAlchemy
        with db_engine.connect() as db_connection:
            # Test 1: Subconsulta
            start_time = time.perf_counter()
            df_sub = pd.read_sql_query(query_subquery, con=db_connection)
            sub_duration = (time.perf_counter() - start_time) * 1000

            # Test 2: JOIN
            start_time = time.perf_counter()
            df_join = pd.read_sql_query(query_join, con=db_connection)
            join_duration = (time.perf_counter() - start_time) * 1000

            # Procesa los resultados si ambas consultas trajeron datos
            if not df_sub.empty and not df_join.empty:
                logging.info(
                    "⚙️  ==== INICIANDO PROCESAMIENTO Y LÓGICA "
                    "INTEGRADA DE NEGOCIO ===="
                )
                print("\n✅ Datos cargados exitosamente.")
                print(
                    "\n==== RESULTADO: SUBCONSULTA Vs JOIN " "(SQL + SQLALCHEMY) ===="
                )
                print(
                    f"📊 Resultados de la Auditoria ({len(df_sub)}) "
                    "registros obtenidos:"
                )
                print(f"⏱️  Tiempo Subconsulta: {sub_duration:.3f} ms.")
                print(f"⏱️  Tiempo JOIN: {join_duration:.3f} ms.")
                print("\n")
                db_engine.dispose()
                return True
            else:
                logging.info(
                    "❌ No se encontraron registros en alguna " "de las tablas."
                )
                print("\n")
                return False

    except Exception as e:
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =====================================================================
# BLOQUE 5: PUNTO DE ENTRADA Y EJECUCIÓN PRINCIPAL
# Objetivo: Iniciar el flujo de trabajo cuando se ejecuta este archivo.
# =====================================================================
if __name__ == "__main__":
    execetion_result = benchmark_queries()
    if isinstance(benchmark_queries, bool) and not benchmark_queries:
        sys.exit(1)
