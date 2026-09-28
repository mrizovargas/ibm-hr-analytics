# =====================================================================
# Título: Filtro de Empleados con Ingreso Superior al Promedio.
#
# Objetivo: Identificar los empleados cuyos ingresos superan la media.
#
# Descripción: Conecta a la base de datos PostgreSQL, extrae la tabla
# de empleados, calcula el sueldo promedio global y filtra a quienes
# ganan por encima de ese valor.
#
# Archivo Python: day19_pandas_cardinality_solution_a.py
#
# Archivo PNG: day19_pandas_cardinality_solution_a.png
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
# Objetivo: Extraer, procesar y filtrar la información de la base.
# =====================================================================


def comparar_con_agregado() -> bool:
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # a. Obtenemos una conexión segura a la base de datos
        engine = get_secure_engine()

        # b. Leemos la tabla de empleados y la guardamos en memoria
        with engine.connect() as conexion:
            fact_employees = pd.read_sql_table("fact_employees", con=conexion)

        # c. Validamos que la tabla no haya llegado vacía
        if not fact_employees.empty:
            print("✅ Datos cargados exitosamente")
            logging.info(
                "🚀 ==== INICIANDO PROCESAMIENTO Y LÓGICA INTEGRADA" " DE NEGOCIO ===="
            )

            # d. Calculamos el promedio de la columna 'monthly_income' y guardamos
            #    ese número único en la variable 'promedio_ingreso' para usarlo
            #    como punto de comparación.
            promedio_ingreso = fact_employees["monthly_income"].mean()

            # e. Buscamos en la tabla a las personas cuyo sueldo sea mayor al
            #    promedio calculado y seleccionamos solo sus identificadores
            #    y salarios para el reporte final.
            df_resultado_a = fact_employees.loc[
                fact_employees["monthly_income"] > promedio_ingreso,
                ["employee_number", "monthly_income"],
            ]

            # f. Mostramos en pantalla un resumen de los resultados
            total_filas = len(df_resultado_a)
            print(f"\n Total de registros encontrados: {total_filas}")
            print("\n👀 Vista previa:")
            print(df_resultado_a.head().to_string(index=False))
            print("\n")

            # g. Cerramos la conexión activa y notificamos éxito
            engine.dispose()
            return True

        else:
            # h. En caso de que la tabla no tenga registros
            logging.info("❌ No se encontraron registros en la tabla.")
            print("\n")
            return False

    except Exception as e:
        # i. Capturamos cualquier falla técnica e interrumpimos
        logging.error(f"❌ Error detectado en: {e}")
        print("\n")
        sys.exit(1)


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y EJECUCIÓN DEL SCRIPT
# Objetivo: Controlar la ejecución del programa cuando se corre directo.
# =====================================================================

if __name__ == "__main__":
    # 1. Ejecutamos la función principal y guardamos la respuesta
    df_comparar_con_agregado = comparar_con_agregado()

    # 2. Si ocurrió una falla o no hubo datos, cerramos con error (1)
    if isinstance(df_comparar_con_agregado, bool) and not df_comparar_con_agregado:
        sys.exit(1)
