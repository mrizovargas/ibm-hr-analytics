# =============================================================================
# Título: Pipeline integrado de automatización e ingesta de datos de RRHH
#
# Objetivo: Garantizar el flujo seguro, la limpieza y la carga de datos de
# empleados.
#
# Descripción: Este script prepara el entorno del sistema, busca y valida un
# archivo CSV con información de recursos humanos, estandariza sus columnas,
# corrige valores inválidos y lo guarda de forma segura en PostgreSQL.
#
# Archivo Python: dat07_main_pipeline_02.py
#
# Arxhico PNG: dat07_main_pipeline_02.png
# =============================================================================

# =========================================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y HERRAMIENTAS ---
# =========================================================
import sys  # Permite interactuar directamente con el sistema operativo y sus rutas
import os  # Proporciona funciones para manipular carpetas y archivos en el disco
import pandas as pd  # Herramienta principal para leer, limpiar y procesar tablas de datos
from dotenv import (
    load_dotenv,
)  # Carga de forma segura contraseñas y variables ocultas desde un archivo .env
from pathlib import (
    Path,
)  # Facilita la creación y el manejo de rutas de archivos en cualquier sistema operativo
import logging  # Permite mostrar y registrar mensajes informativos en la consola sobre el avance del script
import re  # Motor de expresiones regulares utilizado para buscar y transformar patrones de texto

# ================================================================
# --- BLOQUE 2: CONFIGURACIÓN DE RUTAS DEL SISTEMA Y SEGURIDAD ---
# ================================================================
# Encuentra la ubicación de este archivo y sube un nivel para identificar la carpeta raíz del código fuente
src_dir = str(Path(__file__).resolve().parents[1])

# Si la carpeta del código fuente no está registrada en el sistema, la añade para que Python pueda encontrarla
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importa una función personalizada encargada de gestionar la conexión segura a la base de datos
from custom_functions.security_engine import get_secure_engine
from day07_automated_etl_data_flow.day07_traceability_engine import (
    get_trazability_logger,
)

# Activa las variables de entorno ocultas (credenciales, contraseñas, accesos)
load_dotenv()

# Configura el formato de los mensajes en consola, añadiendo la hora exacta, el tipo de mensaje y su contenido
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ===================================================
# --- BLOQUE 3: PIPELINE PRINCIPAL DE INTEGRACIÓN ---
# ===================================================
def execute_traceable_pipeline():
    logging.info("🚀 [Fase 1/3] Iniciando Auditoría de Seguridad y Entorno...")
    try:
        log = get_trazability_logger()
        # Intenta inicializar el motor de conexión segura
        engine = get_secure_engine()
        logging.info(" ====== SEGURIDAD & ENTORNO ======")
        logging.info("✅ variables de entorno validadas. Conexión segura establecida.")
    except Exception as e:
        # Si la seguridad falla, muestra un error crítico y detiene por completo la ejecución del script
        logging.info(f"❌ CRÍTICO: Error en Fase 1 (Seguridad). Pipeline abortado: {e}")
        print("\n")
        sys.exit(1)

    logging.info("⏳ [Fase 2/3] Ejecutando Validación Lógica e Ingesta...")

    try:
        # ===========================================================
        # --- BLOQUE 4 (LÓGICO): RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
        # ===========================================================
        # Busca la ubicación del archivo actual y sube 3 carpetas para llegar a la raíz del proyecto
        base_dir = Path(__file__).resolve().parents[3]

        # Construye la ruta hacia la carpeta específica donde se guardan los datos crudos de RRHH
        target_raw_dir = base_dir / "02_data" / "raw" / "rrhh"

        # Define el nombre del archivo de datos sin la extensión
        rrhh_file_name = "WA_Fn-UseC_-HR-Employee-Attrition"

        # Une la ruta de la carpeta y el nombre del archivo con la extensión .csv
        rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

        # Revisa si el archivo CSV realmente existe en la ruta calculada antes de continuar
        if not os.path.exists(rrhh_path_csv):
            raise FileNotFoundError(
                f"❌ INGESTA: Archivo de origen no localizado en la ruta: {rrhh_path_csv}"
            )

        try:
            # ========================================================
            # --- BLOQUE 5 (LÓGICO): REGLAS DE CONVERSIÓN DE TEXTO ---
            # ========================================================
            # Función interna para convertir nombres tipo 'ColumnaEjemplo' a 'columna_ejemplo'
            def to_snake_case(name):
                """
                Convierte un texto de formato CamelCase o PascalCase a snake_case.
                """
                # Inserta un guion bajo entre una letra minúscula y una mayúscula (ej: "EmpleadoId" -> "Empleado_Id")
                s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)

                # Controla números o mayúsculas juntas y pasa todo el texto a letras minúsculas
                return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

            # ============================================================
            # --- BLOQUE 6 (LÓGICO): CARGA Y NORMALIZACIÓN DE COLUMNAS ---
            # ============================================================
            try:
                logging.info(" ====== INGESTA ======")
                logging.info("⏳ Leyendo archivo CSV original...")
                # Lee el archivo de texto CSV y lo transforma en una tabla digital manipulable (DataFrame)
                df = pd.read_csv(rrhh_path_csv)

                logging.info("🛠️ Limpiando y transformando datos...")
                # Transforma los títulos de todas las columnas usando la función de conversión anterior
                df.columns = [to_snake_case(col) for col in df.columns]

                # Corrige manualmente el caso especial de la columna 'over18' para que coincida con la base de datos
                df.rename(columns={"over18": "over_18"}, inplace=True)

                # Elimina espacios en blanco innecesarios al inicio o al final de cualquier texto en la tabla
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

            except Exception as e:
                # Registra en bitácora si ocurrió un problema durante la carga física o el renombrado
                logging.info(f"❌ Error al cargar o procesar el Dataset: {e}")
                print("\n")

            target_id = 9999
            if target_id in df["employee_number"].values:
                meta = {
                    "target_id": target_id,
                    "found": True,
                    "total_rows_source": len(df),
                }
                log.info(
                    f"Registro objetivo localizado en el CSV de origen.",
                    extra={"data_meta": meta},
                )

            # =========================================================
            # --- BLOQUE 7 (LÓGICO): LIMPIEZA Y VALIDACIÓN DE DATOS ---
            # =========================================================
            # Asegura que el número de empleado sea numérico; si hay errores o textos, pone un 0 temporal
            df["employee_number"] = pd.to_numeric(
                df["employee_number"], errors="coerce"
            ).fillna(0)

            # Asegura que la edad sea un número válido; reemplaza errores con 0
            df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

            # Asegura que los ingresos mensuales sean numéricos; reemplaza errores con 0
            df["monthly_income"] = pd.to_numeric(
                df["monthly_income"], errors="coerce"
            ).fillna(0)

            # Asegura que los años en la empresa sean numéricos; reemplaza errores con 0
            df["years_at_company"] = pd.to_numeric(
                df["years_at_company"], errors="coerce"
            ).fillna(0)

            # Asegura que los años totales trabajados sean numéricos; reemplaza errores con 0
            df["total_working_years"] = pd.to_numeric(
                df["total_working_years"], errors="coerce"
            ).fillna(0)

            # Filtra la tabla para quedarse solo con empleados mayores de edad y con un sueldo real mayor a cero
            df_clean = df[(df["age"] >= 18) & (df["monthly_income"] > 0)]

            # Muestra un reporte en consola indicando cuántos registros pasaron exitosamente los filtros de calidad
            logging.info(
                f"📊 Registros limpios listos para cargar: {len(df_clean)} de {len(df)}"
            )

            # ====================================================
            # --- BLOQUE 8 (LÓGICO): CARGA EN LA BASE DE DATOS ---
            # ====================================================
            # Verifica una última vez que la conexión sea segura antes de intentar transferir la información
            if not get_secure_engine():
                logging.info("❌ Error: El entorno no es seguro o faltan credenciales.")
                print("\n")
                return False

            logging.info("🗄️ Entorno verificado. Conectando a PostgreSQL...")
            logging.info("🗄️ Transfiriendo registros hacia PostgreSQL...")
            logging.info(
                f"📦 Cargando {len(df_clean)} registros y {len(df_clean.columns)} columnas..."
            )

            # Obtiene el motor de conexión activo para realizar la operación
            engine = get_secure_engine()

            # Abre un bloque de transacción que asegura que los datos se guarden por completo, o no se guarde nada si hay error
            with engine.begin() as connection:
                # Escribe la tabla limpia en la base de datos bajo el nombre 'employee_master_data'
                df_clean.to_sql(
                    name="employee_master_data",  # Nombre de la tabla destino en la base de datos
                    con=connection,  # Conexión activa a utilizar
                    if_exists="replace",  # Si la tabla ya existía, la borra y la crea desde cero con datos nuevos
                    index=False,  # No guarda la columna de índices automáticos de Pandas
                    chunksize=500,  # Divide la carga en paquetes de 500 filas para no saturar la memoria
                )

            logging.info("====== TRANSFERENCIA COMPLETA ======")
            logging.info("✅ Datos transferidos a PostgreSQL exitosamente.")
            logging.info(
                f"📦 Total: {len(df_clean)} registros y {len(df_clean.columns)} columnas guardados con éxito."
            )
            logging.info(
                "🎉 [Fase 3/3] Sincronización Exitosa. Datos listos para el consumo de BI."
            )
            return True

        except Exception as error_proceso:
            # Captura y reporta cualquier error que suceda durante el procesamiento o la inserción a la base de datos
            logging.info(
                f"❌ INGESTA: Error crítico detectado durante el proceso: {error_proceso}"
            )
            print("\n")
            return False

    except Exception as e:
        # Captura errores catastróficos de lectura/escritura iniciales y detiene el programa de inmediato
        logging.info(f"❌ CRÍTICO: Error en Fase 2 (Ingesta). Pipeline abortado: {e}")
        print("\n")
        sys.exit(1)


# =======================================
# --- BLOQUE 9: DISPARADOR AUTOMÁTICO ---
# =======================================
# Cláusula estándar que le dice a Python que ejecute la función si este archivo se abre de forma directa
if __name__ == "__main__":
    execute_traceable_pipeline()
