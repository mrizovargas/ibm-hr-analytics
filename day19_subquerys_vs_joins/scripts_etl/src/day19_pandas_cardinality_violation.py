# =========================================================================
# Título: Detección de Error por Violación de Cardinalidad en Pandas
#
# Objetivo: Demostrar cómo la comparación directa entre un valor escalar
# y una Serie completa en Pandas genera un ValueError durante la ejecución.
#
# Descripción: Conecta a PostgreSQL, extrae empleados a un DataFrame e
# intenta evaluar una condición escalar sobre una columna, capturando el
# error correspondiente en la bitácora del sistema.
#
# Archivo Python: day19_pandas_cardinality_violation.py
#
# Archivo PNG: day19_pandas_cardinality_violation.png
# =========================================================================

# =========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar los módulos necesarios y ajustar las rutas del sistema.
# =========================================================================

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

# =========================================================================
# BLOQUE 2: DEFINICIÓN DEL PIPELINE DE PROCESAMIENTO Y VALIDACIÓN
# Objetivo: Conectar a la base de datos y simular el fallo de cardinalidad.
# =========================================================================


def violacion_cardinalidad() -> bool:
    """Extrae la tabla de empleados e intenta evaluar una condición de

    comparación escalar sobre una Serie completa para capturar el error.
    """
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Motor seguro de conexión
        engine = get_secure_engine()

        # Abrir conexión
        with engine.connect() as conexion:
            # Cargar tabla de hechos
            fact_employees = pd.read_sql_table("fact_employees", conexion)

        # Liberar recursos del motor
        engine.dispose()

        # Validar si el DataFrame contiene datos
        if not fact_employees.empty:
            logging.info(
                "🚀 ==== INICIANDO PROCESAMIENTO Y LÓGICA INTEGRADA " "DE NEGOCIO ===="
            )
            print("\n")
            print("✅ Datos cargados exitosamente.")

            # Intentar operación escalar no válida
            try:
                # Extraer columna de ingresos
                valores_multiples = fact_employees["monthly_income"]

                # Comparación ambigua de Serie vs escalar (genera ValueError)
                if valores_multiples > 0:
                    pass
                return True

            except ValueError as ve:
                # Capturar de forma explícita el error de evaluación
                print("\n")
                logging.error(
                    "❌ Error detectado durante la ejecución en "
                    f"Python/Pandas: \n{ve}"
                )
                print("\n")
                sys.exit(1)

        else:
            # Alerta si la tabla está vacía
            logging.info("❌ No se encontraron registros en la tabla.")
            print("\n")
            return False

    except Exception as e:
        # Registro de error genérico y salida de emergencia
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =========================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN PRINCIPAL
# Objetivo: Controlar el flujo de arranque del script al ser ejecutado.
# =========================================================================

if __name__ == "__main__":
    # Iniciar flujo principal
    df_violacion_cardinalidad = violacion_cardinalidad()

    # Validar código de salida
    if isinstance(df_violacion_cardinalidad, bool) and not df_violacion_cardinalidad:
        sys.exit(1)
