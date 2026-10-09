# =====================================================================
# Título: Generación de Diccionario de Datos del Modelo Estrella
#
# Objetivo: Consultar la estructura de la base de datos y exportarla a
# un archivo en formato Markdown.
#
# Descripción: Extrae metadatos de PostgreSQL con SQL, procesa los
# resultados con pandas y guarda la documentación con respaldo y fecha.
#
# Archivo Python: day21_generate_markdown_dictionary.py
#
# Archivo MD: day21_generate_markdown_dictionary.md
#
# Archivo PNG: day21_generate_markdown_dictionary_1.png
#              day21_generate_markdown_dictionary_2.png
# =====================================================================

# =====================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN DEL ENTORNO
# Objetivo: Cargar módulos necesarios y ajustar rutas del proyecto.
# =====================================================================

import pandas as pd  # Manejo y procesamiento de datos
import sys  # Control del sistema operativo e intérprete
import logging  # Bitácoras y registro de mensajes de estado
from datetime import datetime  # Para registrar fechas y horas exactas
from pathlib import Path  # Gestión de rutas absolutas y relativas
from sqlalchemy import text  # Ejecución de consultas SQL seguras

# Agrega la ruta principal para importar módulos personalizados
source_path = str(Path(__file__).resolve().parents[1])
if source_path not in sys.path:
    sys.path.insert(0, source_path)

# Carga de utilidades de bitácora y conexión a la base de datos
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Definimos de forma dinámica la ruta donde se guardarán los resultados
base_dir = Path(__file__).resolve().parents[3]
target_results_dir = base_dir / "10_docs" / "day21_erd_documentation"
get_logging_pipeline()  # Inicializa el registro de eventos


# =====================================================================
# BLOQUE 2: FUNCIÓN PRINCIPAL Y GENERACIÓN DE DICCIONARIO
# Objetivo: Consultar metadatos y exportar la estructura a Markdown.
# =====================================================================


def generate_markdown_dictionary() -> bool:
    """Extrae el diccionario de datos y genera un reporte Markdown."""
    print("\n")  # Salto de línea
    logging.info("==== INICIANDO CONEXIÓN CON POSTGRESQL ====")
    try:
        db_engine = get_secure_engine()  # Genera conexión a PostgreSQL

        # Consulta de metadatos para las tablas seleccionadas
        sql_query = text("""
            SELECT 
                t.table_name AS "Tabla",                  -- Nombre de la tabla consultada
                c.column_name AS "Columna",                -- Nombre del campo o columna
                c.data_type AS "Tipo de Dato",                -- Tipo de dato (e.g., integer, varchar)
                c.is_nullable AS "Permite Null",           -- Acepta valores vacíos (YES/NO)
                COALESCE(
                    tc.constraint_type, 
                    'ATTRIBUTE'
                ) AS tipo_restriccion                    -- Muestra la regla (PK/FK) o 'ATTRIBUTE'
            FROM 
                information_schema.tables AS t           -- Vista principal de tablas
            JOIN 
                information_schema.columns AS c          -- Relaciona las columnas de cada tabla
                ON t.table_name = c.table_name
                AND t.table_schema = c.table_schema
            LEFT JOIN 
                information_schema.key_column_usage AS kcu -- Cruza campos con reglas/llaves
                ON c.table_name = kcu.table_name
                AND c.column_name = kcu.column_name
                AND c.table_schema = kcu.table_schema
            LEFT JOIN 
                information_schema.table_constraints AS tc -- Obtiene el tipo de restricción
                ON kcu.constraint_name = tc.constraint_name
                AND kcu.table_schema = tc.table_schema
            WHERE 
                t.table_catalog = 'ibm_hr_analytics'      -- Filtra por la base de datos específica
                AND t.table_schema = 'public'             -- Solo en el esquema público
                AND t.table_name IN (                     -- Tablas clave a analizar
                    'fact_employees', 
                    'dim_jobs', 
                    'dim_demographics'
                )
            ORDER BY 
                t.table_name,                            -- Ordena por nombre de tabla
                c.ordinal_position;                      -- Mantiene el orden original de campos
        """)

        # Ejecuta la consulta dentro del contexto de conexión
        with db_engine.connect() as db_connection:
            df_schema_results = pd.read_sql(sql_query, con=db_connection)

            # Valida si la consulta retornó información
            if not df_schema_results.empty:
                logging.info("==== INICIANDO CARGA Y PROCESAMIENTO DE DATOS ====")
                print("\n✅ Datos cargados exitosamente.")

                # Construcción del encabezado de la tabla Markdown
                markdown_content = (
                    "# 📖 Diccionario de Datos del Modelo en Estrella\n\n"
                )
                markdown_content += (
                    "*Este documento fue generado automáticamente por el "
                    "pipeline de ingeniería.*\n\n"
                )

                # Generar tabla Markdown sin requerir la librería tabulate
                headers = df_schema_results.columns.tolist()
                markdown_table = "| " + " | ".join(headers) + " |\n"
                markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

                for _, row in df_schema_results.iterrows():
                    row_values = [
                        str(val) if pd.notna(val) else "" for val in row.values
                    ]
                    markdown_table += "| " + " | ".join(row_values) + " |\n"

                markdown_content += markdown_table

                # Garantiza que el directorio de destino exista
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Genera marca de tiempo actual para el respaldo
                time_stamp = datetime.now().strftime("%Y%m%d")

                # Construye el nombre final y la ruta completa
                file_path = target_results_dir / "day21_generate_markdown_dictionary.md"
                file_path_backup = (
                    target_results_dir
                    / f"day21_generate_markdown_dictionary_{time_stamp}.md"
                )

                # Guarda el resultado en el archivo especificado
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                with open(file_path_backup, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                print(f"✅ Diccionario generado exitosamente en: " f"{file_path}")
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
    execution_result = generate_markdown_dictionary()  # Inicia flujo

    # Evalúa si la ejecución retornó un resultado no exitoso
    if isinstance(execution_result, bool) and not execution_result:
        sys.exit(1)  # Aborta la ejecución
