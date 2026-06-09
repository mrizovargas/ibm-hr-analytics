# ==============================================================================
# Título: Pipeline de Extracción, Transformación y Carga (ETL) para Datos de RRHH
#
# Objetivo: Automatizar la ingesta y limpieza de un dataset de recursos humanos.
#
# Descripción: El script localiza, lee, estandariza (formato snake_case) y limpia
# espacios en los datos de empleados de IBM, preparándolos para su posterior
# análisis o inserción en una base de datos.
#
# Arcihvo Python: etl_pipeline.py
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import pandas as pd  # Herramienta principal para la manipulación y análisis de datos.
import os  # Permite interactuar con el sistema operativo y manejar rutas de archivos.
from pathlib import (
    Path,
)  # Utilidad para el manejo seguro y moderno de rutas de directorios.
import re  # Biblioteca para el uso de expresiones regulares y manipulación de texto.
import sys  # Proporciona acceso a variables y funciones que interactúan con el intérprete.
import logging  # Herramienta estándar para registrar mensajes de estado, alertas y errores.

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Localiza la carpeta 'src' subiendo un nivel desde la ubicación de este archivo.
src_dir = str(Path(__file__).resolve().parents[1])

# Registra esa carpeta en el sistema para que Python sepa dónde buscar otros módulos propios.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


# ================================================
# --- BLOQUE 2.1: IMPORTACIONES PERSONALIZADAS ---
# ================================================
# Importa la función para activar el sistema de mensajes informativos (logs) del equipo.
from custom_functions.logging_pipeline import get_logging_pipeline

# Inicializa el registro de logs para documentar el proceso del pipeline.
get_logging_pipeline()


def import_dataset():
    """Función principal que ejecuta de manera secuencial los pasos de lectura y limpieza."""
    try:
        # ===================================================
        # --- BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
        # ===================================================
        # Localiza la carpeta principal del proyecto subiendo tres niveles desde este archivo.
        # Se mantiene como objeto Path para poder usar el operador '/'
        base_dir = Path(__file__).resolve().parents[3]

        # Define la ruta exacta de la carpeta donde se guardan los datos originales de RRHH.
        target_raw_dir = base_dir / "02_data" / "raw" / "rrhh"

        # Guarda el nombre base del archivo CSV de IBM que vamos a procesar.
        rrhh_file_name = "WA_Fn-UseC_-HR-Employee-Attrition"

        # Une la carpeta y el nombre del archivo para obtener la dirección completa en el disco.
        rrhh_path_file = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

        # ===============================================
        # --- BLOQUE 4: LECTURA DE DATOS (EXTRACCIÓN) ---
        # ===============================================
        # Registra en la bitácora (log) que el proceso de lectura ha comenzado.
        print("\n")
        logging.info("====== INICIANDO PROCESO ETL ======")
        logging.info("🔍 Leyendo Dataset de IBM...")

        # Abre el archivo CSV desde su ruta y lo convierte en una tabla digital (DataFrame).
        df = pd.read_csv(rrhh_path_file)

        # ======================================================
        # --- BLOQUE 5: LIMPIEZA Y TRANSFORMACIÓN (FORMATEO) ---
        # ======================================================
        # Registra en la bitácora que inicia la fase de limpieza y transformación.
        logging.info("🛠️ Limpiando y transformando datos...")

        # Función interna para convertir nombres tipo 'ColumnaEjemplo' a 'columna_ejemplo' (snake_case).
        def to_snake_case(name):
            """Convierte un texto de formato CamelCase o PascalCase a snake_case."""
            # Inserta un guion bajo entre una letra minúscula y una mayúscula que inicia una nueva palabra.
            s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            # Maneja casos con números o mayúsculas consecutivas y convierte todo el texto a minúsculas.
            return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

        # ===================================
        # --- BLOQUE 6: CARGA DEL DATASET ---
        # ===================================
        # Registra en la bitácora el inicio de la estandarización de columnas.
        logging.info("🛠️ Carga y normalización de datos...")

        # Transformamos todos los nombres de las columnas al formato 'snake_case' para estandarizar.
        df.columns = [to_snake_case(col) for col in df.columns]

        # Renombra la columna 'over18' a 'over_18' para asegurar coincidencia estricta con la base de datos (DDL).
        df.rename(columns={"over18": "over_18"}, inplace=True)

        # Revisa cada celda: si el valor es texto, elimina los espacios sobrantes al inicio y al final.
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Registra que el proceso de carga y limpieza finalizó exitosamente.
        logging.info("✅ Carga del Dataset completado con éxito.")
        print("\n")

        # Devuelve el dataframe con la estructura y datos ya procesados.
        return df

    # Gestión de errores: Si el archivo no se encuentra en la ruta especificada.
    except FileNotFoundError as e:
        logging.error(f"❌ Archivo no encontrado. Verifica la ruta: {e}")
        print("\n")

    # Gestión de errores general: Ataja cualquier otro fallo durante la lectura o transformación.
    except Exception as e:
        logging.error(f"❌ Error al cargar o procesar el dataset: {e}")
        print("\n")


# ==================================
# --- BLOQUE 7: PUNTO DE ENTRADA ---
# ==================================
# Asegura que el script solo ejecute la función principal si se ejecuta directamente, y no al ser importado por otro código.
if __name__ == "__main__":
    import_dataset()
