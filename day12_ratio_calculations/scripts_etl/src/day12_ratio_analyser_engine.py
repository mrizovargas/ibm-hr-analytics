# ============================================================================
# Título: Pipeline de Verificación y Exportación de Deserción Laboral
#
# Objetivo: Descargar, auditar y guardar el cálculo de la tasa de rotación.
#
# Descripción: Este programa se conecta de forma segura a la base de datos,
# extrae la información de los empleados por departamento, calcula la tasa de
# deserción directamente en Python para auditar los datos, valida que no
# existan errores matemáticos e instala un archivo final en formato CSV con la
# estampa del día y la hora.
#
# Archivo Python: day_ratio_analyser_engine.py
#
# Archivo CSV: day_ratio_analyser_engine.csv
#
# Archivo PNG: day_ratio_analyser_engine.png
# ============================================================================

# ===========================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas y utilidades necesarias para el programa.
# ===========================================================================
import pandas as pd  # Herramienta principal para manejar y procesar tablas.
import numpy as np  # Operaciones matemáticas avanzadas y manejo de nulos.
import logging  # Sistema de registro para dejar un historial de acciones.
import sys  # Permite interactuar con el sistema operativo de la máquina.
import os  # Ayuda a manejar carpetas y rutas de archivos del sistema.
from pathlib import (
    Path,
)  # Facilita la creación y manipulación de rutas de archivos.
from datetime import (
    datetime,
)  # Permite capturar la fecha y hora actual del proceso.

# ==============================================================================
# BLOQUE 2: CONFIGURACIÓN DEL ENTORNO Y RUTAS
# Objetivo: Asegurar que el programa sepa dónde buscar componentes y carpetas.
# ==============================================================================

# Busca la ubicación de este archivo en la computadora y sube un par de
# niveles para encontrar la carpeta del proyecto.
src_dir = str(Path(__file__).resolve().parents[1])

# Si el sistema no tiene registrada esta carpeta, la agrega al inicio para
# poder usar funciones propias del proyecto.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importamos la herramienta interna que nos permite conectarnos a la base
# de datos de manera segura y encriptada.
from custom_functions.security_engine import get_secure_engine

# Definimos la carpeta principal del proyecto subiendo tres niveles desde
# la posición actual.
base_dir = Path(__file__).resolve().parents[3]

# Creamos la ruta exacta donde se guardarán los resultados finales en la
# carpeta de Recursos Humanos (rrhh).
target_results_dir = base_dir / "05_results" / "rrhh" / "day12_ratio_calculations"


# ==============================================================================
# BLOQUE 3: FUNCIÓN PRINCIPAL DE AUDITORÍA Y PROCESAMIENTO
# Objetivo: Conectarse a la base de datos, calcular las métricas y exportarlas.
# ==============================================================================
def verify_attrition_ratios():
    try:
        # 3.1. Conexión de seguridad
        # Activamos el motor de conexión segura para entrar a la base de
        # datos sin exponer contraseñas.
        engine = get_secure_engine()

        # 3.2. Consulta de información
        # Escribimos la orden para pedir el departamento, el puesto, el
        # personal actual y las bajas.
        query = """
            SELECT
                department,
                job_role,
                total_headcount,
                total_bajas
            FROM
                view_attrition_rate_base              
        """

        # Ejecutamos la orden y guardamos la información descargada en una
        # tabla virtual dentro de Python.
        df = pd.read_sql(query, con=engine)

        # 3.3. Procesamiento y Cálculo Analítico
        # Verificamos que la tabla que descargamos no venga vacía.
        if not df.empty:
            print("\n")
            # Dejamos una marca en el historial indicando que la auditoría y el
            # procesamiento de datos ha comenzado.
            logging.info("====== INICIA AUDITORÍA Y PROCESAMIENTO DE DATOS ======")

            # Calculamos el porcentaje de deserción: multiplicamos las bajas
            # por 100 y dividimos entre el total de personal.
            # Nota de seguridad: si un puesto no tiene personal (0), lo
            # cambiamos temporalmente por "vacío" para no romper el programa.
            df["python_attrition_rate"] = (df["total_bajas"] * 100) / df[
                "total_headcount"
            ].replace(0, np.nan)

            # Si algún resultado quedó vacío debido al paso anterior, lo
            # rellenamos con un valor de 0.0 y lo redondeamos a 2 decimales.
            df["python_attrition_rate"] = (
                df["python_attrition_rate"].fillna(0.0).round(2)
            )

            # 3.4. Auditoría de Calidad
            # Verificamos de forma estricta que ningún cálculo haya dado
            # como resultado un valor infinito por error.
            assert not np.isinf(
                df["python_attrition_rate"]
            ).any(), "Error Crítico: Se detectaron valores infinitos en el ratio"

            # Contamos cuántas filas o combinaciones de puestos y áreas
            # procesamos con éxito.
            total_records = len(df)
            # Guardamos un mensaje en el historial confirmando que la
            # revisión de datos fue exitosa y sin fallas.
            logging.info(
                f"✅ Auditoría RAM completada: Se encontraron un total de "
                f"{total_records} matrices evaluadas sin inconsistencias "
                f"numéricas."
            )

            # Mostramos en la pantalla del usuario los primeros 5 renglones
            # de la tabla para dar una vista rápida.
            print("\n 👀 Vista previa:")
            print(df.head())

            # 3.5. Almacenamiento y Cierre
            try:
                # Si las carpetas finales donde queremos guardar el reporte
                # no existen en la computadora, las creamos automáticamente.
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Creamos una etiqueta de tiempo con el año, mes, día, hora,
                # minuto y segundo actual.
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Diseñamos el nombre exclusivo del archivo final usando la
                # etiqueta de tiempo creada.
                target_processed_name = f"day12_ratio_analyser_engine_{timestamp}.csv"
                # Unimos la ruta de la carpeta con el nombre del archivo
                # para saber su ubicación exacta.
                target_processed_path = target_results_dir / target_processed_name

                print("\n")
                # Dejamos constancia en el historial de que vamos a empezar
                # a guardar el archivo.
                logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

                # Guardamos la tabla en formato CSV, sin incluir números de
                # renglón y asegurando caracteres universales (UTF-8).
                df.to_csv(target_processed_path, index=False, encoding="UTF-8")

                # Dejamos notas de éxito en el historial detallando dónde
                # quedó guardado y cómo se llama el archivo.
                logging.info(
                    f"💾 Resultado exportado con éxito en: " f"{target_results_dir}"
                )
                logging.info(f"📄 CSV: {target_processed_name}")

                print("\n")
                # Avisamos al sistema que todo el proceso concluyó con éxito.
                return True

            # Si ocurre un problema exclusivo al guardar el archivo (por
            # ejemplo, falta de permisos), se activa esta alerta.
            except Exception as ex_export:
                logging.error(f"❌ Alerta: No se pudo exportar el archivo: {ex_export}")
                print("\n")
                return False

        # Si desde el principio la base de datos no arrojó ninguna fila, el
        # programa avisa aquí y se detiene de forma segura.
        else:
            logging.info("✨ No se encontraron registros para exportar.")
            print("\n")
            return False

    # Si ocurre un error inesperado en cualquier parte del código, este
    # bloque atrapa la falla y la anota en el historial.
    except Exception as e:
        logging.error(f"❌ Fallo detectado en: {e}")
        return False


# ==============================================================================
# BLOQUE 4: DISPARADOR DEL PROGRAMA (Punto de Entrada)
# Objetivo: Arrancar el programa de forma automática si se ejecuta este archivo.
# ==============================================================================
if __name__ == "__main__":
    # Ejecutamos la función principal; si llega a fallar o no encuentra
    # datos, detiene todo el sistema con un código de error (1).
    if not verify_attrition_ratios():
        sys.exit(1)
