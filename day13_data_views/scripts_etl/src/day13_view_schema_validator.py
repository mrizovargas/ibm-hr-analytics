# =====================================================================
# Título: Pipeline de Auditoría e Integridad para Datos de RH
#
# Objetivo: Verificar la estructura y respaldar la vista de personal.
#
# Descripción: Este programa se conecta de forma segura a la base de
# datos, extrae la información de la vista corporativa de analítica
# de Recursos Humanos y audita que contenga exactamente las columnas
# requeridas. Si la estructura es correcta, toma una fotografía de los
# datos (snapshot) y la exporta a un archivo CSV con la fecha y hora
# exacta de la ejecución para mantener un control de cambios limpio.
#
# Archivo Python: day13_view_schema_validator.py
#
# Archivo CSV: day13_view_snapshot_audit.csv
#
# Archivo PNG: day13_view_schema_validator.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para el programa.
# =====================================================================
# Pandas nos ayuda a manipular y estructurar datos en tablas.
import pandas as pd

# Sys permite interactuar con el sistema operativo del equipo.
import sys

# Logging registra el paso a paso del script para auditorías.
import logging

# Datetime nos ayuda a capturar la fecha y hora en tiempo real.
from datetime import datetime

# Path ayuda a manejar rutas de archivos sin importar el sistema.
from pathlib import Path

# =====================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que el programa sepa dónde buscar carpetas.
# =====================================================================
# Buscamos la carpeta contenedora del código del proyecto.
src_dir = str(Path(__file__).resolve().parents[1])

# Si la carpeta no está en la lista de búsqueda de Python, la añade.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Traemos funciones creadas por nosotros para seguridad y logs.
from custom_functions.security_engine import get_secure_engine
from custom_functions.logging_pipeline import get_logging_pipeline

# Localizamos la carpeta principal de todo nuestro proyecto.
base_dir = Path(__file__).resolve().parents[3]
# Definimos la carpeta exacta donde guardaremos los reportes de RH.
target_results_dir = base_dir / "05_results" / "rrhh" / "day13_data_views"

# Encendemos nuestra bitácora para empezar a registrar acciones.
get_logging_pipeline()


# ==============================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL DE AUDITORÍA Y PROCESAMIENTO
# Objetivo: Conectarse a la base de datos, procesamiento de datos y exportación.
# ==============================================================================
def audit_view_integrity():
    """Ejecuta la revisión de calidad y el respaldo de la vista."""
    print("\n")
    logging.info(
        "🚀 ==== INICIANDO ESCANEO DE INTEGRIDAD " "(view_corporate_hr_analytics) ===="
    )
    try:
        # 3.1. Conexión de seguridad
        # Conectamos de forma segura a la base de datos corporativa.
        engine = get_secure_engine()

        # 3.2. Consulta de información
        # Preparamos la orden en SQL para traer todos los datos de RH.
        query = """
            SELECT *
            FROM view_corporate_hr_analytics;
        """

        # Traemos la información y la convertimos en una tabla estructurada.
        df = pd.read_sql(query, con=engine)

        # 3.3. Procesamiento
        # Verificamos que la tabla que descargamos no venga vacía.
        if not df.empty:
            logging.info("==== INICIA AUDITORÍA Y PROCESAMIENTO DE DATOS ====")

            # Esta es la lista de columnas oficiales que deberíamos tener.
            columnas_esperadas = [
                "id_empleado",
                "num_empleado",
                "puesto",
                "edad",
                "estatus_baja",
                "sueldo_mensual",
                "flag_horas_extra",
                "indice_permanencia_rol",
            ]
            # Extraemos los nombres de las columnas que llegaron realmente.
            columnas_reales = list(df.columns)

            # 3.4. Auditoría de Calidad
            # Comparamos ambas listas; si no coinciden, detenemos todo.
            assert columnas_reales == columnas_esperadas, (
                "❌ Falla de integridad: Las columnas de la vista "
                "no coinciden con el diseño oficial."
            )

            # Si pasamos el assert, celebramos que todo está en orden.
            logging.info("✅ Validación de metadatos aprobada con éxito.")

            # Mostramos en pantalla una pequeña muestra de las filas.
            print("\n👀 Vista previa: ")
            print(df.head())

            # 3.5. Almacenamiento y Cierre
            try:
                # Si la carpeta de destino no existe, la creamos.
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Creamos una marca de tiempo con formato AñoMesDía_Hora...
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Diseñamos el nombre final de nuestro archivo de respaldo.
                target_processed_name = f"day13_view_snapshot_audit_{time_stamp}.csv"
                # Unimos la ruta de la carpeta con el nombre del archivo.
                target_processed_path = target_results_dir / target_processed_name

                print("\n")
                logging.info("==== INICIA EXPORTACIÓN DE DATOS A CSV ====")

                # Guardamos la tabla como un archivo CSV seguro y universal.
                df.to_csv(target_processed_path, index=False, encoding="UTF-8")

                # Registramos en el log que todo se guardó correctamente.
                logging.info(
                    f"💾 Snapshot de control guardado con {len(df)} "
                    "registros procesados."
                )
                logging.info(
                    "💾 Resultado exportado con éxito en: " f"{target_results_dir}"
                )
                logging.info(f"📄 CSV: {target_processed_name}")

                print("\n")
                return True

            # Si algo falla al guardar el archivo, atrapamos el error aquí.
            except Exception as e_export:
                logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
                print("\n")
                return False

        # Si la tabla llegó vacía desde la base de datos, avisamos aquí.
        else:
            logging.info("✨ No se encontraron registros para validar.")
            print("\n")
            return False

    # Si la base de datos está caída o la consulta falla, cae aquí.
    except Exception as e:
        logging.info(f"❌ Fallo detectado en: {e}")
        return False


# =====================================================================
# BLOQUE 4: DISPARADOR DEL PROGRAMA
# Objetivo: Asegurar que el script corra solo si lo ejecutamos directo.
# =====================================================================
if __name__ == "__main__":
    # Si la auditoría da error, cerramos el programa avisando al sistema.
    if not audit_view_integrity():
        sys.exit(1)
