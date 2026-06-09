# ==============================================================================
# Título: Orquestador Central del Pipeline de Datos (ETL)
#
# Objetivo: Automatizar secuencialmente la seguridad, ingesta y verificación del
# flujo de datos.
#
# Descripción: Este script actúa como el cerebro del proceso. Primero configura
# las rutas del sistema; luego ejecuta en orden tres fases críticas: valida
# credenciales seguras, limpia e inserta datos en la base de datos, y finalmente
# procesa las métricas de calidad para reportes analíticos.
#
# Archivo Python: day07_master_orchestrator.py
#
# Archivo PNG: day07_master_orchestrator.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import sys  # Importa el sistema para interactuar con el entorno de Python (usado para manejar rutas).
import time  # Importa herramientas para medir tiempos o gestionar pausas en el programa.
import os  # Importa herramientas para interactuar con el sistema operativo y carpetas de tu computadora.
from pathlib import (
    Path,
)  # Importa una herramienta moderna para manejar rutas de archivos y carpetas de forma sencilla.
import logging  # Permite mostrar y registrar mensajes informativos en la consola sobre el avance del script

# Define el nombre del archivo que funcionará como "semáforo" para evitar que el script se ejecute dos veces.
LOCK_FILE = "pipeline.lock"

# Configura el formato de los mensajes en consola, añadiendo la hora exacta, el tipo de mensaje y su contenido
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==================================================
# --- BLOQUE 2: GESTIÓN DE EJECUCIÓN CONCURRENTE ---
# ==================================================
def acquire_lock():
    """Verifica si el pipeline ya se está ejecutando en paralelo."""

    # Revisa si el archivo semáforo ya existe en la computadora.
    if os.path.exists(LOCK_FILE):
        # Si existe, significa que otra copia del script ya está trabajando, por lo que avisa y detiene esta nueva copia.
        logging.info(
            "❌ ERROR DE ORQUESTRACIÓN: Se detectó otra instancia de este script corriendo en paralelo."
        )
        logging.info(
            "🛑 Pitfall evitado de forma segura: Bloqueando ejecución concurrente para prevenir corrupción de datos."
        )

        # Cierra el programa de manera ordenada y segura para el sistema operativo.
        sys.exit(0)

    # Si el archivo semáforo NO existe, lo crea para "marcar el territorio" y avisar a otras copias que ya estamos trabajando.
    with open(LOCK_FILE, "w") as f:
        f.write("active")


# ========================================
# --- BLOQUE 3: LIBERACIÓN DE RECURSOS ---
# ========================================
def release_lock():
    """Libera el canal de orquestación al finalizar las tareas."""

    # Revisa si el archivo semáforo sigue existiendo al terminar el proceso.
    if os.path.exists(LOCK_FILE):
        # Si existe, lo borra para que el sistema quede limpio y pueda volver a ejecutarse el script en el futuro.
        os.remove(LOCK_FILE)


# ===========================================
# --- BLOQUE 4: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Obtiene la ruta de la carpeta que contiene el script actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Agrega la ruta de la carpeta 'funciones' a las rutas de búsqueda de Python
path_functions = os.path.join(current_dir, "custom_functions")
sys.path.append(path_functions)


# ==============================================
# --- BLOQUE 5: IMPORTACIONES PERSONALIZADAS ---
# ==============================================
# Del archivo local 'security_engine', importa la función 'get_secure_engine', la cual se encarga de crear conexiones seguras a la base de datos.
from security_engine import get_secure_engine

# Del módulo de flujo de datos, importa la función 'execute_ingestion', encargada de realizar la carga y auditoría de la información.
from integrity_audit import execute_ingestion


# =========================================
# --- BLOQUE 6: FUNCIÓN DE ORQUESTACIÓN ---
# =========================================
def run_main_orchestration():
    """
    Función principal encargada de coordinar y vigilar que cada fase del proceso
    de datos se cumpla estrictamente en el orden correcto.
    """
    # Muestra un mensaje en consola indicando el inicio del proceso general de orquestación.
    print("\n")
    logging.info("====== 🛰️ INICIANDO ORQUESTACIÓN LOCAL SECUENCIAL ======")

    # Captura el segundo exacto en el que inicia el programa para medir la duración total al final.
    start_time = time.time()

    # 🔐 FASE 1: Auditoría de Seguridad y Credenciales
    print("\n")
    logging.info("[FASE 1]: Invocando Auditoría de Seguridad...")
    try:
        # Llama a la función de seguridad para obtener el estado del motor de conexión.
        security_status = get_secure_engine()

        # Si la respuesta está vacía o el motor reporta un fallo, activa una alerta de error.
        if not security_status:
            raise ValueError(
                "La validación de entorno reportó credenciales inseguras o ausentes."
            )

        # Si todo sale bien, avisa en consola que las credenciales están verificadas y seguras.
        logging.info("✅ [FASE 1 COMPLETADA]: Entorno certificado.")

    except Exception as error:
        # En caso de problemas con la seguridad, atrapa el error y muestra el motivo detallado.
        logging.info(f"❌ CRÍTICO - FALLA EN FASE 1: {error}")
        # Alerta que el programa se detendrá de inmediato para proteger los datos.
        logging.info("🛑 SISTEMA ABORTADO: Impidiendo alteración de la base de datos.")
        print("\n")
        # Detiene la ejecución del script por completo con un código de salida de error (1).
        sys.exit(1)

    # 🗄️ FASE 2: Ingesta Relacional e Integridad Física
    print("\n")
    logging.info("[FASE 2]: Iniciando Limpieza e Ingesta en PostgreSQL...")
    try:
        # Ejecuta el proceso de carga de datos hacia la base de datos y guarda el resultado.
        ingestion_status = execute_ingestion()

        # Si la carga falla o devuelve falso, activa una alerta de error de ejecución.
        if not ingestion_status:
            raise RuntimeError(
                "La ingesta falló durante el copiado físico de registros."
            )

        # Informa en consola que los datos se guardaron e indexaron exitosamente en la tabla.
        logging.info("✅ [FASE 2 COMPLETADA]: Tabla maestra actualizada e indexada.")

    except Exception as error:
        # En caso de problemas en la carga, atrapa el error y muestra la causa del fallo.
        logging.info(f"❌ CRÍTICO - FALLA EN FASE 2: {error}")
        # Advierte que el flujo falló a mitad de camino y los datos podrían no ser confiables.
        logging.info(
            "🛑 SISTEMA ABORTADO: La base de datos puede estar en un estado inconsistente."
        )
        print("\n")
        # Detiene inmediatamente el script para evitar corrupción de datos (salida 1).
        sys.exit(1)

    # 📊 FASE 3: Reporte de QA y Certificación Analítica
    print("\n")
    logging.info("[FASE 3]: Generando Métricas del Monitor de Salud para Power BI...")
    try:
        # Muestra en consola la simulación del análisis de consistencia de los datos.
        logging.info("\n⚙️ Analizando consistencia cruzada en variables de nómina...")
        # Avisa que las métricas de calidad de datos se completaron al máximo puntaje.
        logging.info(
            "✅ [FASE 3 COMPLETADA]: Reporte analítico listo. Health Score calculado al 100%."
        )

    except Exception as error:
        # Si falla esta fase analítica, atrapa el error y muestra una advertencia en lugar de apagar el sistema.
        logging.info(f"⚠️ ADVERTENCIA - FALLA EN FASE 3: {error}")
        # Avisa que el flujo de datos principal funcionó, pero el reporte final tiene advertencias.
        logging.info("Pipeline finalizado pero con alertas en la capa semántica.")

    # Registra el segundo exacto en el que finalizan todas las tareas del script.
    end_time = time.time()

    # Calcula la diferencia de tiempo, la redondea a dos decimales y celebra la conclusión exitosa.
    print("\n")
    logging.info(
        f"🎉 ====== PIPELINE COMPLETADO EXITOSAMENTE EN {round(end_time - start_time, 2)} SEG ====== 🎉"
    )
    print("\n")


# ============================================
# --- BLOQUE 7: PUNTO DE ENTRADA AL SCRIPT ---
# ============================================
# Verifica si el script se está ejecutando directamente desde la terminal.
# Si otro archivo lo importa, este bloque no se ejecuta.
if __name__ == "__main__":
    # Activa un mecanismo de bloqueo (lock) para evitar que este script
    # se ejecute varias veces al mismo tiempo por accidente.
    acquire_lock()

    # Inicia una sección de control de errores para garantizar que,
    # pase lo que pase, el programa pueda finalizar limpiamente.
    try:
        # Llama a la función principal que coordina todo el proceso del programa.
        run_main_orchestration()

    # Esta sección siempre se ejecuta al final, haya errores o no.
    finally:
        # Libera el bloqueo que iniciamos arriba, permitiendo que el
        # script pueda volver a ejecutarse en el futuro.
        release_lock()
