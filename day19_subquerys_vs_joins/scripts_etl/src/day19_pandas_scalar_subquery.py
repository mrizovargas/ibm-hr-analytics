# =====================================================================
# Título: Filtrado de Empleados con Salario Superior al Promedio con
# Pandas
#
# Objetivo: Consultar la tabla de empleados desde PostgreSQL para
# identificar quienes ganan más que el ingreso mensual promedio y
# mostrar los resultados ordenados.
#
# Descripción: El pipeline establece una conexión segura a la base de
# datos, extrae la información de los empleados en un DataFrame de
# Pandas, calcula el salario promedio global, filtra a los empleados que
# superan ese promedio y presenta una vista previa limpia ordenada de
# mayor a menor ingreso.
#
# Archivo Python: day19_pandas_scalar_subquery.py
#
# Archivo PNG: day19_pandas_scalar_subquery.png
# =====================================================================


# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar módulos necesarios y agregar rutas del sistema.
# =====================================================================

# Manipulación de datos
import pandas as pd

# Control del sistema y script
import sys

# Registro de eventos y logs
import logging

# Gestión de rutas de archivos
from pathlib import Path

# Obtener e incluir la ruta raíz del proyecto
src_dir = str(Path(__file__).resolve().parents[1])
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Conexión segura y sistema de logs
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Inicializar logs
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DEL PIPELINE DE PROCESAMIENTO
# Objetivo: Conectar a la base de datos, procesar y filtrar la información.
# =====================================================================


def scalar_sq_pandas() -> bool:
    """Extrae datos de empleados y puestos, filtra salarios
    superiores al promedio y muestra el resultado ordenado.
    """
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Motor seguro de conexión
        engine = get_secure_engine()

        # Abrir conexión
        with engine.connect() as conexion:
            # Cargar tablas de hechos y dimensiones
            fact_employees = pd.read_sql_table("fact_employees", con=conexion)
            dim_jobs = pd.read_sql_table("dim_jobs", con=conexion)

            # Validar que ambas tablas contengan datos
            if not (fact_employees.empty or dim_jobs.empty):
                logging.info(
                    "🚀 ==== INICIANDO PROCESAMIENTO Y LÓGICA INTEGRADA "
                    "DE NEGOCIO ===="
                )
                print("\n✅ Datos cargados exitosamente.")

                # Paso 1: Salario promedio global (AVG)
                promedio_salario = fact_employees["monthly_income"].mean()

                # Paso 2: Filtrar salarios que superan el promedio (WHERE > AVG)
                df_filtrado = fact_employees[
                    fact_employees["monthly_income"] > promedio_salario
                ]

                # Paso 3: Cruzar con puestos para obtener departamento y rol (INNER JOIN)
                df_merge = df_filtrado.merge(
                    dim_jobs[["job_id", "department", "job_role"]],
                    on="job_id",
                    how="inner",
                )

                # Paso 4: Seleccionar columnas finales
                columnas_deseadas = [
                    "employee_number",
                    "department",
                    "job_role",
                    "monthly_income",
                ]

                # Paso 5: Ordenar por ingreso descendente (ORDER BY DESC)
                df_resultado_pandas = df_merge[columnas_deseadas].sort_values(
                    by="monthly_income", ascending=False
                )

                # Imprimir vista previa
                print(
                    "\n==== RESULTADO PANDAS + SQLALCHEMY: "
                    "Empleados con Salario > Promedio ===="
                )

                # Mostrar total y vista previa
                total_filas = len(df_resultado_pandas)
                print(f"\nTotal de registros encontrados: {total_filas}")
                print("\n👀 Vista Previa:")
                print(df_resultado_pandas.head().to_string(index=False))
                print("\n")

                # Liberar recursos y finalizar
                engine.dispose()
                return True

            else:
                # Alerta si alguna tabla está vacía
                logging.info("❌ No se encontraron registros en la tabla principal.")
                print("\n")
                return False

    except Exception as e:
        # Registro de error y salida de emergencia
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN PRINCIPAL
# Objetivo: Iniciar el flujo de trabajo cuando se ejecuta este archivo.
# =====================================================================

if __name__ == "__main__":
    # Iniciar flujo principal
    df_scalar_sq_pandas = scalar_sq_pandas()

    # Validar código de salida
    if isinstance(df_scalar_sq_pandas, bool) and not df_scalar_sq_pandas:
        sys.exit(1)
