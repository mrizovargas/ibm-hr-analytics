# ==============================================================================
# Título: Pipeline de Registro y Procesamiento
#
# Objetivo: Demostrar el flujo básico de un proceso de datos automatizado,
# asegurando que todas las acciones y posibles errores queden registrados para
# su análisis.
#
# Decripción: El script utiliza un sistema de bitácora (logging) que guarda cada
# paso importante en la consola. Esto permite saber exactamente qué está haciendo
# el programa en tiempo real, confirmar si el proceso terminó con éxito o, en caso
# de fallar, identificar el problema de inmediato.
#
# Archivo Python: logging_pipeline.py
#
# Archivo PNG: logging_pipeline.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
import logging  # Para mostrar mensajes de estado organizados en la consola.

# ======================================================================
# --- BLOQUE 2 (LÓGICO): CONFIGURACIÓN SISTEMA DE REGISTRO (LOGGING) ---
# ======================================================================


def get_logging_pipeline():
    """Función principal que ejecuta el pipeline de procesamiento."""

    # Se verifica si el sistema ya tiene configuraciones previas para evitar mensajes duplicados.
    if not logging.getLogger().hasHandlers():
        # Se establece el nivel mínimo de importancia que se va a registrar (INFO)
        logging.basicConfig(
            level=logging.INFO,
            # Se define cómo se verá el mensaje: incluye la hora, el tipo de alerta y el texto
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    # Marca el inicio del proceso en la bitácora
    # print("\n")
    # logging.info("====== INICIANDO LOGGING PIPELINE ======")

    # ========================================================
    # --- BLOQUE 3 (LÓGICO): EJECUCIÓN Y MANEJO DE ERRORES ---
    # ========================================================
    try:
        # Registra en la bitácora que el paso anterior fue exitoso
        # logging.info(
        # "✅ Configuración del formato 'Sistema de Registro' (Logging) completado con éxito."
        # )

        # Devuelve el resultado final del proceso
        return True

    # Si algo sale malo durante el bloque "try", el programa salta aquí
    except Exception as e:
        # Registra un mensaje de error detallando qué causó el fallo
        logging.error(f"❌ Alerta: El pipeline falló debido a: {e}")
        print("\n")

        # Detiene el programa por completo y relanza el error para ser notificados
        raise


# ===========================================
# --- BLOQUE 4 (LÓGICO): PUNTO DE ENTRADA ---
# ===========================================
# Este bloque asegura que el pipeline se ejecute automáticamente al correr el archivo
if __name__ == "__main__":
    get_logging_pipeline()
