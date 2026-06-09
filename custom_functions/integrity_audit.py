# ==============================================================================
# Título: Proceso de Ingesta y Limpieza de Datos de Recursos Humanos
#
# Objetivo: Automatizar la carga, depuración y transferencia del archivo de
# empleados.
#
# Descripción: Este script localiza el archivo CSV original de RRHH, estandariza
# sus columnas a un formato limpio, filtra registros inválidos (como menores de
# edad o ingresos en cero) y exporta el resultado final depurado hacia una base
# de datos PostgreSQL.
#
# Archivo Python: integrity_audit.py
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
# Herramienta fundamental para manipular y analizar datos en formato de tabla.
import pandas as pd

# Biblioteca nativa para interactuar con el sistema operativo y carpetas de tu computadora.
import os

# Biblioteca para buscar, extraer o reemplazar patrones complejos de texto.
import re

# Proporciona acceso a variables y funciones que interactúan directamente con el intérprete de Python.
import sys

# Módulo moderno y sencillo para manejar rutas de archivos y directorios.
from pathlib import Path

# Permite mostrar y registrar mensajes informativos en la consola sobre el avance del script
import logging

# Módulo para trabajar con fechas y horas (por ejemplo, obtener la fecha actual o dar formato al tiempo)
from datetime import datetime

# Módulo moderno para interactuar con el sistema de archivos y manejar rutas de carpetas/archivos de forma multiplataforma
from pathlib import Path

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Obtiene la ruta de la carpeta que contiene el script actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Agrega la ruta de la carpeta 'funciones' a las rutas de búsqueda de Python
path_functions = os.path.join(current_dir, "custom_functions")
sys.path.append(path_functions)

# Configura el formato de los mensajes en consola, añadiendo la hora exacta, el tipo de mensaje y su contenido
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==============================================
# --- BLOQUE 3: IMPORTACIONES PERSONALIZADAS ---
# ==============================================
# Ahora puedes importar el archivo .py que tiene la función
from security_engine import get_secure_engine, test_connection


def execute_ingestion() -> bool:
    # ===========================================================
    # --- BLOQUE 4 (LÓGICO): RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
    # ===========================================================
    # Busca la ubicación del archivo actual y sube 3 carpetas para llegar a la raíz del proyecto
    base_dir = Path(__file__).resolve().parents[3]

    # Construye la ruta hacia la carpeta específica donde se guardan los datos crudos de RRHH
    target_raw_dir = base_dir / "02_data" / "raw" / "rrhh"

    # Ruta destino para guardar los registros descartados o con errores de lógica corporativa
    target_discarded_dir = base_dir / "02_data" / "processed" / "rejected" / "rrhh"

    # Define el nombre del archivo de datos sin la extensión
    rrhh_file_name = "WA_Fn-UseC_-HR-Employee-Attrition"

    # Une la ruta de la carpeta y el nombre del archivo con la extensión .csv
    rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

    # Revisa si el archivo CSV realmente existe en la ruta calculada antes de continuar
    if not os.path.exists(rrhh_path_csv):
        logging.info("❌ ====== INGESTA ======")
        logging.info(f"Archivo de origen no localizado en la ruta: {rrhh_path_csv}")
        print("\n")
        # Detiene el programa y retorna False porque no hay datos para procesar
        return False

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
            logging.info("====== INGESTA ======")
            logging.info("⏳ Leyendo archivo CSV original...")
            # Lee el archivo de texto CSV y lo transforma en una tabla digital manipulable (DataFrame)
            df = pd.read_csv(rrhh_path_csv)

            logging.info("🛠️ Limpiando y transformando datos...")
            # Transforma los títulos de todas las columnas usando la función de conversión anterior
            df.columns = [to_snake_case(col) for col in df.columns]

            # Corrige manualmente el caso especial de la columna 'over18' para que coincida con la base de datos
            df.rename(columns={"over18": "over_18"}, inplace=True)

            # Recorre cada celda de la tabla y, si es un texto, le borra los espacios vacíos de los extremos
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        except Exception as e:
            # Captura fallos específicos de la lectura o del formateo inicial de las columnas
            logging.info(f"❌ Error al cargar o procesar el Dataset: {e}")
            print("\n")
            return False

        # =========================================================
        # --- BLOQUE 7 (LÓGICO): LIMPIEZA Y VALIDACIÓN DE DATOS ---
        # =========================================================
        # Convierte la columna a número; si hay texto inválido lo vuelve vacío y luego lo rellena con 0
        df["employee_number"] = pd.to_numeric(
            df["employee_number"], errors="coerce"
        ).fillna(0)

        # Repite el proceso de conversión a número y limpieza para la edad
        df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

        # Repite el proceso de conversión a número y limpieza para el ingreso mensual
        df["monthly_income"] = pd.to_numeric(
            df["monthly_income"], errors="coerce"
        ).fillna(0)

        # Repite el proceso de conversión a número y limpieza para los años en la empresa
        df["years_at_company"] = pd.to_numeric(
            df["years_at_company"], errors="coerce"
        ).fillna(0)

        # Repite el proceso de conversión a número y limpieza para el total de años trabajados
        df["total_working_years"] = pd.to_numeric(
            df["total_working_years"], errors="coerce"
        ).fillna(0)

        # Definimos las condiciones de validez corporativa
        valid_age = df["age"] >= 18
        valid_income = df["monthly_income"] > 0

        # Filtramos los registros limpios usando ambas condiciones concurrentes
        df_clean = df[valid_age & valid_income]

        # Obtenemos el inverso exacto de la condición para capturar los registros inválidos
        df_invalid = df[~(valid_age & valid_income)]

        # Evaluamos el volumen de registros descartados
        df_discarded = len(df_invalid)

        # Evalúa el resultado con la condicional if
        if df_discarded > 0:
            if df_discarded == 1:
                logging.info(
                    f"⚠️ Se ha detectado {df_discarded} fila que no cumple con las reglas de negocio establecidas (Edad < 18 / Salario <= 0)"
                )
            else:
                logging.info(
                    f"⚠️ Se han detectado {df_discarded} filas que no cumplen con las reglas de negocio establecidas (Edad < 18 / Salario <= 0)"
                )

            # Procedemos a exportar las filas con fallas de integridad a la carpeta destino
            try:
                # Crea de forma segura la estructura de directorios si aún no existe en el disco duro
                target_discarded_dir.mkdir(parents=True, exist_ok=True)

                # Obtenemos la fecha y hora exactas para crear un identificador
                # Formato: AñoMesDía_HoraMinutoSegundo (ej. 20260523_153900)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Genera una ruta de destino para el archivo que contiene errores o rechazos.
                discared_file_name = f"rejected_{rrhh_file_name}_{timestamp}.csv"
                discarded_file_path = target_discarded_dir / discared_file_name

                # Exportamos a formato CSV sin el índice por defecto de pandas
                df_invalid.to_csv(discarded_file_path, index=False, encoding="utf-8")
                logging.info(
                    f"💾 Respaldo de auditoría exportado con éxito en: {discarded_file_path}"
                )
                logging.info(f"📄 CSV: {discared_file_name}")

            except Exception as e_export:
                logging.info(
                    f"❌ Alerta: No se pudo exportar el archivo de auditoría local: {e_export}"
                )
                print("\n")
        else:
            logging.info(
                "✨ Perfecto. El 100% de los registros cumplen con las reglas de negocio iniciales."
            )

        # Muestra en la pantalla un resumen de cuántas filas superaron los filtros de limpieza
        logging.info(
            f"📊 Registros limpios listos para cargar: {len(df_clean)} de {len(df)}"
        )

        # ====================================================
        # --- BLOQUE 8 (LÓGICO): CARGA EN LA BASE DE DATOS ---
        # ====================================================
        # Validamos que el entorno sea seguro
        if not get_secure_engine():
            logging.info("❌ Error: El entorno no es seguro o faltan credenciales.")
            print("\n")
            return False

        logging.info("🗄️ Entorno verificado. Conectando a PostgreSQL...")

        test_connection()

        logging.info("🗄️ Transfiriendo registros hacia PostgreSQL...")
        # Muestra un aviso con la cantidad exacta de filas y columnas limpias que se van a subir
        logging.info(
            f"📦 Cargando {len(df_clean)} registros y {len(df_clean.columns)} columnas..."
        )

        # Llama al motor de seguridad externo para obtener los accesos validados de la base de datos
        engine = get_secure_engine()

        # Guarda la tabla limpia en PostgreSQL, reemplaza si ya existía y sube los datos en bloques de 500 en 500
        with engine.begin() as connection:
            # engine.begin() maneja automáticamente un COMMIT si todo sale bien,
            # o un ROLLBACK completo si ocurre un error a mitad de la carga.
            df_clean.to_sql(
                name="employee_master_data",
                con=connection,
                if_exists="replace",
                index=False,
                chunksize=500,
            )

        logging.info("✅ ====== TRANSFERENCIA COMPLETA ======")
        # Confirma el éxito de la operación mostrando el conteo final enviado a la base de datos
        logging.info(
            f"📦 Total: {len(df_clean)} registros y {len(df_clean.columns)} columnas guardados con éxito."
        )
        return True

    except Exception as error_proceso:
        # Atrapa cualquier error inesperado en el flujo (como caídas de red o fallas del motor SQL)
        logging.info(
            f"❌ INGESTA: Error crítico detectado durante el proceso: {error_proceso}"
        )
        print("\n")
        return False


# ===========================================
# --- BLOQUE 9 (LÓGICO): PUNTO DE ENTRADA ---
# ===========================================
# Verifica si el script se está abriendo directamente (y no importado desde otro archivo)
if __name__ == "__main__":
    logging.info("🏃 Ejecutando prueba local aislada de ingesta...")
    # Lanza la función principal para procesar y cargar los datos
    execute_ingestion()
