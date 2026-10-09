# =====================================================================
# Título: Generación de Diccionario de Datos del Modelo Estrella
#
# Objetivo: Extraer los metadatos de las tablas del modelo estrella en
# PostgreSQL y exportarlos a un archivo con formato Markdown.
#
# Descripción: Consulta la estructura de las tablas clave del esquema
# público, procesa sus columnas y tipos de datos, y genera un documento
# MD formateado como tabla.
#
# Archivo Python: day21_inf_schema_cols.py
#
# Archivo PNG: day21_inf_schema_cols.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar módulos necesarios y ajustar rutas del proyecto.
# =====================================================================

import pandas as pd  # Manejo y procesamiento de datos
import sys  # Control del sistema operativo e intérprete
import logging  # Bitácoras y registro de mensajes de estado
from datetime import datetime  # Para registrar fechas y horas exactas.
from pathlib import Path  # Gestión de rutas absolutas y relativas
from sqlalchemy import text  # Ejecución de consultas SQL seguras

# Agrega la ruta principal para importar módulos personalizados
source_path = str(Path(__file__).resolve().parents[1])
if source_path not in sys.path:
    sys.path.insert(0, source_path)

# Carga de utilidades de bitácora y conexión a la base de datos
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Definimos de forma dinámica la ruta donde se guardarán los resultados (tres niveles arriba).
base_dir = Path(__file__).resolve().parents[3]
target_results_dir = base_dir / "10_docs" / "day21_erd_documentation"

get_logging_pipeline()  # Inicializa el registro de eventos


# =====================================================================
# BLOQUE 2: FUNCIÓN PRINCIPAL Y GENERACIÓN DE DICCIONARIO
# Objetivo: Consultar metadatos y exportar la estructura a Markdown.
# =====================================================================


def inf_schema_cols() -> bool:
    """Extrae el diccionario de datos y genera un reporte Markdown."""
    print("\n")  # Salto de línea
    logging.info("==== INICIANDO CONEXIÓN CON POSTGRESQL ====")
    try:
        db_engine = get_secure_engine()  # Genera conexión a PostgreSQL

        # Consulta de metadatos para las tablas seleccionadas
        sql_query = text("""
            SELECT
                table_name,
                column_name,
                data_type,
                is_nullable
            FROM
                information_schema.columns
            WHERE
                table_catalog = 'ibm_hr_analytics'
                AND table_schema = 'public'
                AND table_name IN ('fact_employees', 'dim_jobs', 'dim_demographics')
            ORDER BY
                table_name,
                ordinal_position;
        """)

        # Ejecuta la consulta dentro del contexto de conexión
        with db_engine.connect() as db_connection:
            df_schema_results = pd.read_sql(sql_query, con=db_connection)

            # Valida si la consulta retornó información
            if not df_schema_results.empty:
                logging.info("==== INICIANDO CARGA Y PROCESAMIENTO DE DATOS ====")
                print("\n✅ Datos cargados exitosamente.")

                # Construcción del encabezado de la tabla Markdown
                markdown_output = "## Diccionario de Datos del Modelo\n\n"
                markdown_output += (
                    "| Tabla | Columna | Tipo de Dato | Permite Nulos |\n"
                )
                markdown_output += "|---|---|---|---|\n"

                # Recorre las filas del DataFrame usando itertuples()
                for row in df_schema_results.itertuples(index=False):
                    markdown_output += (
                        f"| **{row.table_name}** | `{row.column_name}` | "
                        f"`{row.data_type}` | {row.is_nullable} |\n"
                    )

                # Garantiza que el directorio de destino exista
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Genera una marca de tiempo actual (AñoMesDía_HoraMinutoSegundo) para el nombre del archivo.
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Construye el nombre final y la ruta completa del archivo MD.
                file_name = "day_21_data_dictionary"
                file_path = target_results_dir / f"{file_name}.md"
                file_path_backup = target_results_dir / f"{file_name}_{time_stamp}.md"

                # Guarda el resultado en el archivo especificado
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(markdown_output)

                with open(file_path_backup, "w", encoding="utf-8") as f:
                    f.write(markdown_output)

                print(f"💾 Diccionario generado exitosamente en: {target_results_dir}")
                print(f"📄 MD: {file_name}")
                print("\n")
                db_engine.dispose()  # Cierra conexiones
                return True
            else:
                logging.info("❌ No se encontraron registros en la tabla.")
                print("\n")
                return False

    except Exception as e:
        logging.error(f"❌ Error detectado en: {e}")  # Registra la falla
        print("\n")
        sys.exit(1)  # Finaliza script con error


# =====================================================================
# BLOQUE 3: PUNTO DE ENTRADA Y CONTROL DE EJECUCIÓN
# Objetivo: Ejecutar la función principal y controlar errores.
# =====================================================================

if __name__ == "__main__":
    execution_result = inf_schema_cols()  # Inicia el flujo

    # Evalúa si la ejecución retornó un resultado no exitoso
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)  # Aborta la ejecución
