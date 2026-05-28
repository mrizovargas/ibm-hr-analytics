# =====================================================================================
# Título: Pipeline de Detección de Fuga de Talento Crítico
#
# Objetivo: Identificar de forma automatizada al personal en riesgo de abandonar la
# empresa dentro del departamento de Investigación y Desarrollo (R&D) que percibe ingresos
# bajos.
#
# Descripción: Este script se conecta a una base de datos centralizada, extrae la
# información de los empleados y aplica un filtro inteligente de tres criterios. Los
# registros encontrados se guardan inmediatamente en una tabla de alertas en la base de
# datos y se exportan a un archivo CSV con la fecha y hora de ejecución, permitiendo al
# equipo de Recursos Humanos tomar acciones preventivas de retención.
#
# Archivo Python: day08_segmentation_engine.py
#
# Archivo CSV: day08_alert_low_income_attrition.csv
#
# Archivo PNG: day08_segmentation_engine.png
# =====================================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import pandas as pd  # Biblioteca principal para manipular y filtrar tablas de datos.
import sys  # Permite modificar rutas internas del sistema para encontrar otros archivos.
import logging  # Sistema de mensajes que informa lo que hace el programa en tiempo real.
from pathlib import (
    Path,
)  # Facilita la creación y manejo de rutas de carpetas de forma segura.
from datetime import datetime  # Ayuda a capturar la fecha y hora actual del sistema.

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Localiza la carpeta 'src' subiendo un nivel desde la ubicación de este archivo.
src_dir = str(Path(__file__).resolve().parents[1])

# Registra esa carpeta en el sistema para que Python sepa dónde buscar otros módulos propios.
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# ==============================================
# --- BLOQUE 2.1: IMPORTACIONES PERSONALIZADAS ---
# ==============================================
# Trae las funciones del equipo para conectar a la base de datos y activar los mensajes informativos.
from custom_functions.security_engine import get_secure_engine
from custom_functions.logging_pipeline import get_logging_pipeline

# ===================================================
# --- BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
# ===================================================
# Encuentra la carpeta raíz del proyecto subiendo tres niveles completos en el árbol de carpetas.
base_dir = Path(__file__).resolve().parents[3]

# Construye la ruta exacta de la carpeta donde se guardarán los reportes finales de RRHH.
target_results_dir = base_dir / "05_results" / "rrhh" / "day08_advanced_filtering"

# Enciende el sistema centralizado de alertas y mensajes informativos.
get_logging_pipeline()


# ===================================================
# --- BLOQUE 4: PROCESAMIENTO GENERAL DEL PIPELINE ---
# ===================================================
def isolate_critical_talent():
    """
    Función principal que ejecuta la extracción, filtrado y guardado del talento en riesgo.
    """
    try:
        print("\n")
        # Registra el inicio formal de las operaciones con la base de datos.
        logging.info("====== 🗄️ INICIANDO CONEXIÓN A PostgreSQL ======")
        logging.info("⏳ Conectando al motor relacional de PostgreSQL...")

        # Activa y guarda la conexión segura a la base de datos PostgreSQL.
        engine = get_secure_engine()

        # Confirma que la comunicación con el servidor de datos funciona correctamente.
        logging.info("✅ Conexión exitosa al motor relacional de PostgreSQL.")

        # Instrucción en lenguaje de base de datos para solicitar toda la tabla de empleados.
        query = """
            SELECT *
            FROM employee_master_data
        """

        # Trae la tabla completa desde la base de datos y la convierte en un objeto manipulable (DataFrame).
        df = pd.read_sql(query, con=engine)

        print("\n")
        # Inicia el proceso de análisis y separación de los datos.
        logging.info("====== ⚡ INICIANDO FILTRADO MULTI-CRITERIO VECTORIZADO  ======")

        # Define las 3 condiciones de riesgo: departamento específico, indicador de abandono e ingresos bajos.
        condicion_depto = df["department"] == "Research & Development"
        condicion_fuga = df["attrition"] == "Yes"
        condicion_sueldo = df["monthly_income"] <= 5000

        # Aplica los tres filtros al mismo tiempo para aislar únicamente a los empleados que cumplen todo.
        df_radar_critico = df[condicion_depto & condicion_fuga & condicion_sueldo]

        # Verifica si el filtro encontró al menos a una persona en esta situación de riesgo.
        if not df_radar_critico.empty:
            # Informa cuántos empleados críticos fueron detectados en el análisis.
            logging.info(
                f"🎯 Segmentación Completada. Población crítica detectada: {len(df_radar_critico)} empleados."
            )
            print("\n")

            # ========================================================
            # --- BLOQUE 5: EXPORTACIÓN DE RESULTADOS A PostgreSQL ---
            # ========================================================
            # Inicia la fase de almacenamiento de los resultados en el servidor.
            logging.info("====== INICIA EXPORTACIÓN DE DATOS A PostgreSQL ======")

            # Nombre que recibirá la nueva tabla de alertas dentro de la base de datos.
            alert_table_name = "alert_low_income_attrition"

            # Envía la lista de afectados a la base de datos, reemplazando la tabla anterior si ya existía.
            df_radar_critico.to_sql(
                alert_table_name, con=engine, if_exists="replace", index=False
            )
            # Notifica que el guardado digital en el servidor fue exitoso.
            logging.info(
                f"✅ Tabla de alerta {alert_table_name} fué creada con éxito en PostgreSQL."
            )

            # ===================================================
            # --- BLOQUE 6: EXPORTACIÓN DE RESULTADOS A DISCO ---
            # ===================================================
            # Bloque de seguridad secundario para escribir el archivo físico en la computadora.
            try:
                # Crea físicamente la carpeta de destino en el disco duro si aún no existe.
                target_results_dir.mkdir(parents=True, exist_ok=True)

                # Captura el momento exacto (AñoMesDía_HoraMinutoSegundo) para evitar sobrescribir reportes previos.
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Une el nombre base de la alerta con la estampa de tiempo para el archivo final.
                processed_file_name = (
                    f"day08_alert_low_income_attrition_{timestamp}.csv"
                )
                # Define la localización exacta en la computadora donde se guardará este archivo nuevo.
                processed_file_path = target_results_dir / processed_file_name

                print("\n")
                # Comienza la escritura del archivo local.
                logging.info("====== INICIA EXPORTACIÓN DE DATOS A FORMATO CSV ======")

                # Convierte los datos analizados a formato de texto plano CSV usando codificación universal.
                df_radar_critico.to_csv(
                    processed_file_path, index=False, encoding="utf-8"
                )

                # Muestra la confirmación y las rutas exactas donde el usuario puede abrir el reporte final.
                logging.info(
                    f"💾 Resultado exportado con éxito en: {target_results_dir}"
                )
                logging.info(f"📄 CSV: {processed_file_name}")
                print("\n")
                # Finaliza exitosamente la función devolviendo una señal de confirmación.
                return True

            except Exception as e:
                # Si la computadora bloquea el archivo o no hay espacio, registra el problema.
                logging.info(f"❌ Alerta: No se pudo exportar el archivo: {e}")
                print("\n")
                return False

        else:
            # Si el filtro no arrojó ningún empleado en riesgo, finaliza sin generar archivos.
            logging.info("✨ No se encontraron registros que exportar.")
            print("\n")
            return False

    except Exception as e:
        # Registra fallos críticos del sistema, como problemas de red o cambios en la base de datos.
        logging.error(f"❌ Fallo en el motor de segmentación: {e}")
        print("\n")
        return False


# ==================================
# --- BLOQUE 7: PUNTO DE ENTRADA ---
# ==================================
# Lanza el análisis automáticamente si el usuario ejecuta este script de forma directa.
if __name__ == "__main__":
    isolate_critical_talent()
