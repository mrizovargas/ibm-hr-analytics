# =====================================================================
# Título: Pipeline de Auditoría y Validación de Integridad Estructural
#
# Objetivo: Verificar que la normalización de datos no causó pérdidas.
#
# Descripción: Este script se conecta a PostgreSQL para extraer los
# datos de la tabla plana original y los de la nueva tabla de hechos.
# Después, compara que ambas compartan la misma cantidad total de filas
# y exactamente los mismos códigos de empleados, garantizando que el
# proceso fue seguro.
#
# Archivo Python: day15_validar_datos.py
#
# Archivo PNG: day15_validar_datos.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para el programa.
# =====================================================================
# Pandas nos ayuda a estructurar y comparar tablas de datos fácilmente.
import pandas as pd

# Sys permite interactuar con el sistema operativo (como cerrar el script).
import sys

# Logging sirve para guardar un historial de lo que pasa en el programa.
import logging

# Path ayuda a manejar rutas de archivos sin importar el sistema operativo.
from pathlib import Path

# =====================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que el programa sepa dónde buscar carpetas.
# =====================================================================
# Calculamos la ruta de la carpeta raíz del proyecto de forma dinámica.
src_dir = str(Path(__file__).resolve().parents[1])

# Si la ruta raíz no está registrada en el sistema, la añadimos al inicio.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos las herramientas propias creadas para conectar la base de datos
# y configurar los registros de actividad (logs).
from custom_functions.security_engine import get_secure_engine
from custom_functions.logging_pipeline import get_logging_pipeline

# Activamos el sistema de bitácora para registrar el progreso.
get_logging_pipeline()


# =====================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL DE AUDITORÍA
# Objetivo: Conectar, descargar y validar la consistencia de los datos.
# =====================================================================
def validate_normalization():
    # Dejamos un espacio en blanco en la consola para mejorar la lectura.
    print("\n")
    # Registramos que estamos intentando conectar con la base de datos.
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Obtenemos la conexión segura y encriptada hacia la base de datos.
        engine = get_secure_engine()

        # Escribimos la consulta para traer los datos originales en bruto.
        query_sorce = """
            SELECT *
            FROM employee_master_data;
        """
        # Escribimos la consulta para traer los datos ya normalizados.
        query_fact_emp = """
            SELECT *
            FROM fact_employees;
        """

        # Usamos Pandas para ejecutar las consultas y descargar las tablas.
        df_source = pd.read_sql(query_sorce, con=engine)
        df_fact_emp = pd.read_sql(query_fact_emp, con=engine)

        # Primer control: Verificamos que la tabla original no esté vacía.
        if not df_source.empty:
            # Segundo control: Verificamos que la tabla de hechos tenga datos.
            if not df_fact_emp.empty:
                logging.info("====⚡ INICIANDO VALIDACIÓN DE CONSISTENCIA ====")

                # Prueba 1: Comprobamos si ambas tablas tienen las mismas filas.
                if len(df_source) != len(df_fact_emp):
                    print("Prueba 1:")
                    print(f"La tabla origen contiene {len(df_source)} filas.")
                    print(f"La tabla origen contiene {len(df_source)} filas.")
                    logging.error(
                        "❌ ERROR Prueba 1: Pérdida de datos en: fact_employees."
                    )
                    return False

                print("\n")
                print("Prueba 1:")
                print(f"La tabla origen contiene {len(df_source)} filas.")
                print(f"La tabla destino contiene {len(df_fact_emp)} filas.")
                print(
                    "✅ El número de filas entre el origen y el destino coinciden perfectamente."
                )

                # Pasamos los códigos de empleados a conjuntos para compararlos.
                original_ids = set(df_source["employee_number"])
                new_ids = set(df_fact_emp["employee_number"])

                # Prueba 2: Validamos si existen códigos faltantes o distintos.
                if original_ids != new_ids:
                    logging.error(
                        "❌ ERROR Prueba 2: Los IDs de los empleados no coinciden "
                        "entre el origen y el destino."
                    )
                    return False

                print("\n")
                print("Prueba 2:")
                print(
                    "✅ Los IDs de los empleados coinciden perfectamente entre el origen y el destino."
                )

                # Si todo sale bien, registramos el éxito total.
                print("\n")
                logging.info(
                    "✅ VALIDACIÓN EXITOSA: Cero registros perdidos. "
                    "Integridad referencial perfecta."
                )
                print("\n")
                return True

            else:
                # Avisamos si la tabla de destino se encuentra vacía.
                logging.error("No se encontraron registros en: fact_employees.")
                print("\n")
                return False
        else:
            # Avisamos si la tabla de origen se encuentra vacía.
            logging.error("No se encontraron registros en: employee_master_data.")
            print("\n")
            return False

    except Exception as e:
        # Si ocurre un problema inesperado (como falta de red), lo capturamos.
        logging.error(f"Error detectado en: {e}")
        return False


# =====================================================================
# BLOQUE 4: DISPARADOR AUTOMÁTICO DEL SCRIPT
# Objetivo: Ejecutar la validación al abrir el archivo directamente.
# =====================================================================
if __name__ == "__main__":
    # Si la validación falla, cerramos el programa enviando una señal de error.
    if not validate_normalization():
        sys.exit(1)
