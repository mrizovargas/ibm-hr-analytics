# ==============================================================================
# Título: Auditoría de Lógica Condicional y Segmentación de Riesgo de Empleados
#
# Objetivo: Evaluar y clasificar el nivel de riesgo de los empleados.
#
# Descripción: El programa se conecta de forma segura a una base de
# datos de Recursos Humanos, extrae la información laboral, aplica reglas de
# negocio automatizadas para detectar casos de alerta por exceso de horas extra o
# baja satisfacción, y finalmente exporta los resultados en un reporte limpio.
#
# Archivo Python: day10_risk_validator.py
#
# Archivo CSV: day10_risk_validator.csv
#
# Archivo PNG: day10_risk_validator.png
# ==============================================================================

# ==============================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas y utilidades necesarias para el programa.
# ==============================================================================
import pandas as pd  # Herramienta para la manipulación y análisis de datos en tablas
import logging  # Sistema para registrar eventos y mensajes del progreso del programa
import sys  # Funciones para interactuar con el sistema operativo y el entorno de Python
from pathlib import (
    Path,
)  # Utilidad para manejar rutas de archivos de forma limpia y segura
from datetime import (
    datetime,
)  # Herramienta para obtener la fecha y la hora actual del sistema
import time  # Módulo para medir tiempos de ejecución y rendimiento del código
import numpy as np  # Librería para operaciones matemáticas y lógica condicional avanzada

# ==============================================================================
# BLOQUE 2: CONFIGURACIÓN DE ENTORNO
# Objetivo: Asegurar que Python pueda encontrar todos los módulos del proyecto.
# ==============================================================================
# Busca la ruta de la carpeta 'src' subiendo 1 nivel desde el archivo actual para ubicar la raíz
dir_src = str(Path(__file__).resolve().parents[1])

# Añade la carpeta raíz al sistema si no está configurada para que reconozca los scripts personalizados
if dir_src not in sys.path:
    sys.path.insert(0, dir_src)

# ==============================================================================
# BLOQUE 2.1: IMPORTACIONES PERSONALIZADAS
# Objetivo: Traer las funciones específicas creadas para este proyecto.
# ==============================================================================
# Conecta el programa con la base de datos de forma segura protegiendo credenciales
from custom_functions.security_engine import get_secure_engine

# Trae el sistema de bitácoras personalizado para documentar el progreso paso a paso
from custom_functions.logging_pipeline import get_logging_pipeline

# Inicializa la bitácora para empezar a registrar todo el proceso en la consola
get_logging_pipeline()

# ==============================================================================
# BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS
# Objetivo: Definir dónde se guardarán los resultados del análisis.
# ==============================================================================
# Sube tres niveles desde este archivo para localizar la carpeta principal del proyecto
base_dir = Path(__file__).resolve().parents[3]

# Define la ruta exacta dentro del proyecto en dónde se guardarán los reportes procesados
target_results_dir = base_dir / "05_results" / "rrhh" / "day10_conditional_logic"

# Registra el momento exacto en el que empieza el proceso para poder calcular la duración total
inicio_tiempo = time.time()


# ==============================================================================
# BLOQUE 4: FUNCIÓN PRINCIPAL DE AUDITORÍA
# Objetivo: Ejecutar el análisis completo de datos y la exportación.
# ==============================================================================
def audit_conditional_logic():
    # Deja un espacio en blanco en la consola para mejorar la legibilidad visual
    print("\n")

    # Registra en la bitácora que se está iniciando el proceso de conexión
    logging.info("🗄️ ====== INICIANDO CONEXIÓN CON PostgreSQL ======")

    try:
        # Llama a la función segura para conectarse a la base de datos
        engine = get_secure_engine()

        # Calcula el tiempo transcurrido y confirma que la conexión fue exitosa
        logging.info(
            "✅ Conexión con PostgreSQL establecida en %.2f segundos.",
            time.time() - inicio_tiempo,
        )

        # Define la consulta SQL para extraer únicamente las columnas necesarias de Recursos Humanos
        query = """
            SELECT
                employee_id,
                employee_number,
                over_time,
                job_satisfaction,
                years_in_current_role
            FROM
                employee_master_data
        """

        # Ejecuta la consulta SQL y descarga los datos directamente en un DataFrame de Pandas
        df = pd.read_sql(query, con=engine)

        # Verifica si la tabla de datos extraída contiene registros para procesar
        if not df.empty:
            logging.info("====== VALIDACIÓN CRUZADA ====== ")
            logging.info("🚀 Iniciando validación cruzada de lógica secuencial")

            # Define las reglas de negocio para clasificar a los empleados según su situación laboral
            condiciones = [
                # Regla para Riesgo Crítico: Trabaja horas extra, baja satisfacción y menos de un año en el puesto
                (df["over_time"] == "Yes")
                & (df["job_satisfaction"] <= 2)
                & (df["years_in_current_role"] <= 1),
                # Regla para Riesgo Medio: Trabaja horas extra y tiene una satisfacción regular
                (df["over_time"] == "Yes") & (df["job_satisfaction"] == 3),
            ]

            # Define las etiquetas correspondientes a cada una de las condiciones anteriores
            opciones = ["Crítico", "Medio"]

            # Aplica las reglas y crea una nueva columna; si no cumple ninguna, se asigna "Estable"
            df["python_risk_segment"] = np.select(
                condiciones, opciones, default="Estable"
            )

            # Cuenta cuántos empleados fueron clasificados bajo la categoría de "Crítico"
            total_criticos = int((df["python_risk_segment"] == "Crítico").sum())

            # Registra en la bitácora el éxito de la auditoría y el total de casos críticos hallados
            logging.info(
                f"🎯 Auditoria completada con éxito. Empleados en Riesgo Crítico detectados: {total_criticos}"
            )

            # Muestra en la consola una pequeña vista previa de las primeras 5 clasificaciones calculadas
            print("\n")
            print(df.head().to_string(index=False))

            try:
                # Crea la carpeta de destino en tu computadora si aún no existe
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Genera una marca de tiempo con formato AñoMesDía_HoraMinutoSegundo para evitar duplicados
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Construye el nombre final y la ruta completa que tendrá el archivo final CSV
                processed_file_name = f"day10_risk_validator_{time_stamp}.csv"
                processed_path_name = target_results_dir / processed_file_name

                # Deja un espacio e informa que la exportación al archivo físico ha comenzado
                print("\n")
                logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

                # Guarda la columna de resultados en el disco duro asegurando compatibilidad de caracteres (UTF-8)
                df.to_csv(processed_path_name, index=False, encoding="utf-8")

                # Confirma en la bitácora las rutas exactas y nombres del archivo generado con éxito
                logging.info(
                    f"💾 Resultado exportado con éxito en: {target_results_dir}"
                )
                logging.info(f"📄 CSV: {processed_file_name}")
                print("\n")

                # Indica que la función terminó correctamente su ejecución
                return True

            except Exception as e_export:
                # Captura y registra errores específicos si falla la escritura del archivo en el disco
                logging.error(f"❌ Alerta: No se pudo exportar el archivo: {e_export}")
                return False

        else:
            # Informa en caso de que la consulta a la base de datos haya regresado una tabla vacía
            logging.info("✨ No se encontraron registros que exportar.")
            return False

    except Exception as e:
        # Captura y muestra cualquier error general grave del proceso (como fallas de red o de SQL)
        logging.error(f"❌ Error en el proceso de validación: {e}")
        return False


# ==============================================================================
# BLOQUE 5: PUNTO DE ENTRADA DEL SCRIPT
# Objetivo: Garantizar la ejecución ordenada del programa.
# ==============================================================================
if __name__ == "__main__":
    # Ejecuta el análisis; si la función devuelve False o falla, detiene el sistema con un código de error (1)
    if not audit_conditional_logic():
        sys.exit(0)
