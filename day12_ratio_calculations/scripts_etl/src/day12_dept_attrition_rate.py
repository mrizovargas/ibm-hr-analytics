# =================================================================================
# Título: Pipeline de Automatización: Cálculo de Tasa de Deserción por Departamento
#
# Objetivo: Calcular el porcentaje de rotación de personal de forma segura y
# automatizada.
#
# Descripción: El script carga la información histórica de los empleados, agrupa al
# personal por su departamento y calcula cuántos han dejado la empresa. Además,
# incluye un blindaje lógico para evitar fallos por división entre cero si un
# departamento está vacío, guardando el reporte final en un formato limpio (CSV).
#
# Archivo Python: day12_dept_attrition_rate.py
#
# Archivo CSV: day12_dept_attrition_rate.csv
#
# Archivo PNG day12_dept_attrition_rate.png
# =================================================================================

# ===========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas estándar indispensables para el programa.
# ===========================================================================
import pandas as pd  # Herramienta principal para manipular y analizar tablas de datos.
import numpy as np  # Utilizada aquí para controlar valores matemáticos infinitos o nulos.
import sys  # Permite interactuar directamente con el sistema operativo y las rutas de Python.
import os  # Ayuda a manejar tareas del sistema de archivos.
import logging  # Registra el historial de lo que pasa en el programa (bitácora de eventos).
from pathlib import (
    Path,
)  # Facilita la creación y manejo de rutas de carpetas sin importar el sistema operativo.
from datetime import (
    datetime,
)  # Permite capturar la fecha y hora actual para nombrar los archivos finales.

# ==============================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que Python localice los módulos del proyecto y definir carpetas de salida.
# ==============================================================================

# Busca la carpeta raíz del código subiendo dos niveles desde donde está este archivo.
src_dir = str(Path(__file__).resolve().parents[1])

# Si esa carpeta de código no está registrada en Python, la inyectamos en la posición principal (0).
if not src_dir in sys.path:
    sys.path.insert(0, src_dir)

# Importamos funciones personalizadas creadas previamente para el proyecto (carga de datos y bitácora).
from custom_functions.etl_pipeline import import_dataset
from custom_functions.logging_pipeline import get_logging_pipeline

# Definimos la ruta maestra de almacenamiento subiendo tres niveles.
base_dir = Path(__file__).resolve().parents[3]
# Creamos la ruta exacta donde se guardarán los resultados del "Día 12".
target_results_dir = base_dir / "05_results" / "rrhh" / "day12_ratio_calculations"

# Activamos la bitácora personalizada para que empiece a registrar el flujo en la consola.
get_logging_pipeline()


# ==============================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL - PROCESAMIENTO Y CÁLCULO DE RATIOS
# Objetivo: Transformar los datos brutos en métricas de Recursos Humanos.
# ==============================================================================
def tasa_desercion_depto():
    # Descargamos o leemos el set de datos maestros de los empleados.
    df = import_dataset()

    # Verificamos que la tabla no venga vacía antes de hacer cualquier operación.
    if not df.empty:
        logging.info("====== INICIA PROCESAMIENTO DE DATOS ======")

        # Transformamos la columna de texto 'attrition' (Yes/No) a números (1/0) para poder sumarla.
        df["abandono_numerico"] = df["attrition"].apply(
            lambda x: 1 if x == "Yes" else 0
        )

        # Agrupamos la información por área de la empresa y calculamos las sumas y conteos básicos.
        df_depto = (
            df.groupby("department")
            .agg(
                empleados_salieron=(
                    "abandono_numerico",
                    "sum",
                ),  # Suma de todos los que dijeron "Yes".
                plantilla_inicial=(
                    "attrition",
                    "count",
                ),  # Conteo total de personal histórico en esa área.
            )
            .reset_index()
        )  # Aplanamos el resultado para volver a tener una estructura de tabla limpia.

        # PRUEBA DE ESTRÉS (Programación Defensiva):
        # Insertamos a la fuerza un departamento nuevo sin empleados asignados para verificar que el código resiste.
        registro_vacio = pd.DataFrame(
            [
                {
                    "department": "Data Science (Emergente)",
                    "empleados_salieron": 0,
                    "plantilla_inicial": 0,
                }
            ]
        )
        df_depto = pd.concat([df_depto, registro_vacio], ignore_index=True)

        # CÁLCULO DE LA TASA Y PROTECCIÓN ARITMÉTICA:
        # Al dividir entre la plantilla, si esta es 0, Python genera un número infinito (inf).
        # Con '.replace' transformamos de inmediato esos infinitos en valores nulos seguros (NaN), evitando que el script falle.
        df_depto["tasa_desercion"] = (
            df_depto["empleados_salieron"] / df_depto["plantilla_inicial"]
        ).replace([np.inf, -np.inf], np.nan)

        # Mostramos en pantalla cómo quedó nuestra tabla final recalculada.
        print("\n👀 Vista previa:")
        print(df_depto)

        # ==============================================================================
        # BLOQUE 4: EXPORTACIÓN SEGURA A FORMATO CSV
        # Objetivo: Guardar físicamente el reporte garantizando que no se pierdan datos.
        # ==============================================================================
        try:
            # Creamos las carpetas de destino en tu computadora en caso de que aún no existan.
            target_results_dir.mkdir(parents=True, exist_ok=True)

            # Generamos una marca de tiempo única (AñoMesDía_HoraMinutoSegundo) para que los archivos no se encimen.
            time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Definimos el nombre dinámico del archivo final y su ubicación exacta.
            processed_file_name = f"day12_dept_attrition_rate_{time_stamp}.csv"
            processed_file_path = target_results_dir / processed_file_name

            print("\n")
            logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

            # Convertimos la tabla de memoria a un archivo físico .csv con codificación universal de texto.
            df_depto.to_csv(processed_file_path, index=False, encoding="utf-8")

            # Registramos el éxito de la operación en la bitácora de control.
            logging.info(f"💾 Resultado exportado con éxito en: {target_results_dir}")
            logging.info(f"📄 CSV: {processed_file_name}")
            print("\n")
            return True

        # En caso de un problema físico (permisos del disco duro, espacio insuficiente, etc.), capturamos el fallo.
        except Exception as e_export:
            logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
            print("\n")
            return False

    # Si la tabla original del dataset no tenía registros desde el inicio, cancelamos el proceso con gracia.
    else:
        logging.info("✨ No se encontraron registros para exportar.")
        print("\n")
        return False


# ==============================================================================
# DISPARADOR DEL PROGRAMA
# Asegura que la función se ejecute solo si este script se abre directamente.
# ==============================================================================
if __name__ == "__main__":
    # Si la función retorna un error o un False, se detiene el sistema avisándole a la terminal.
    if not tasa_desercion_depto():
        sys.exit(1)
