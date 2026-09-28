# =====================================================================
# Título: Filtro de Empleados por Pertenencia a Lista de Ingresos.
#
# Objetivo: Filtrar empleados cuyos ingresos coincidan con el área de
# Ventas.
#
# Descripción: Conecta a PostgreSQL, lee la tabla maestra, obtiene los
# sueldos del departamento de Sales y filtra a los colaboradores cuyo
# sueldo esté presente en esa lista de valores.
#
# Archivo Python: day19_pandas_cardinality_solution_b.py
#
# Archivo PNG: day19_pandas_cardinality_solution_b.png
# =====================================================================


# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar herramientas y asegurar la ruta base del proyecto.
# =====================================================================

# 1. Herramientas estándar para manipular datos, sistema e historial
# Librería principal para estructuración y manejo de datos en tablas
import pandas as pd

# Módulo nativo del sistema para gestionar la ejecución del script
import sys

# Módulo estándar para registrar eventos e incidencias del programa
import logging

# Herramienta para manipular rutas de archivos de forma independiente al SO
from pathlib import Path

# 2. Obtenemos la ruta raíz del proyecto para importar módulos propios
src_dir = str(Path(__file__).resolve().parents[1])

# 3. Añadimos la ruta al sistema si aún no está registrada
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 4. Importamos funciones internas de seguridad y registro de eventos
from custom_functions.security_engine import get_secure_engine
from custom_functions.logging_pipeline import get_logging_pipeline

# 5. Inicializamos el sistema para guardar el historial de ejecución
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: DEFINICIÓN DE LA FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# Objetivo: Extraer, procesar y comparar datos frente a una lista.
# =====================================================================


def comparar_vs_lista() -> bool:
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # a. Obtenemos una conexión segura a la base de datos
        engine = get_secure_engine()

        # b. Leemos la tabla maestra de empleados y la cargamos en memoria
        with engine.connect() as conexion:
            employee_master_data = pd.read_sql_table(
                "employee_master_data", con=conexion
            )

        # c. Validamos que la tabla contenga información
        if not employee_master_data.empty:
            print("\n")
            print("✅ Datos cargados exitosamente.\n")
            logging.info("🚀 ==== INICIANDO PROCESAMIENTO Y LÓGICA INTEGRADA ====")

            # d. Extraemos la serie de sueldos del equipo de Ventas
            lista_ingresos_validos = employee_master_data.loc[
                employee_master_data["department"] == "Sales", "monthly_income"
            ]

            # e. Filtramos a quienes tengan un sueldo dentro de esa lista
            df_resultado_b = employee_master_data.loc[
                employee_master_data["monthly_income"].isin(lista_ingresos_validos),
                ["employee_number", "job_role", "department", "monthly_income"],
            ]

            # f. Imprimimos el resumen y la vista previa en consola
            total_filas = len(df_resultado_b)
            print(f"\nTotal de registros encontrados: {total_filas}")
            print("\n👀 Vista Preliminar:")
            print(df_resultado_b.head().to_string(index=False))
            print("\n")

            # g. Liberamos la conexión y devolvemos confirmación exitosa
            engine.dispose()
            return True

        else:
            # h. En caso de que la tabla esté completamente vacía
            logging.info("❌ No se encontraron registros en la tabla.")
            print("\n")
            return False

    except Exception as e:
        # i. Capturamos cualquier error en la ejecución e interrumpimos
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Controlar la ejecución del programa cuando se corre directo.
# =====================================================================

if __name__ == "__main__":
    # 1. Ejecutamos la función principal y capturamos su resultado
    df_comparar_vs_lista = comparar_vs_lista()

    # 2. Si la función devolvió False, finalizamos con estado de error (1)
    if isinstance(df_comparar_vs_lista, bool) and not df_comparar_vs_lista:
        sys.exit(1)
