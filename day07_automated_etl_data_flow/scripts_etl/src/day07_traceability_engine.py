# ==============================================================================
# Título: Motor de Trazabilidad Estructurada en JSON
#
# Objetivo: Crear un sistema de registro de eventos (logs) que estructure la
#           información automáticamente en formato JSON.
#
# Descripción: Este script define una herramienta de diagnóstico que captura y
#              organiza datos clave (fecha, nivel de error, módulo y mensaje).
#              Esto facilita el análisis automatizado y la búsqueda de errores
#              en sistemas complejos.
#
# Archivo Python: day07_traceability_engine.py
#
# Archivo PNG: day07_traceability_engine.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================

# Importamos la librería estándar para el registro de eventos y errores
import logging

# Importamos la librería para manipular datos en formato JSON
import json

# Importamos la librería para gestionar el tiempo (útil para las marcas de tiempo)
import time

# =====================================================
# --- BLOQUE 2: FORMATEADOR PERSONALIZADO PARA JSON ---
# =====================================================


# 🛠️ Configuración del formateador para emitir JSON Estructurado
class JsonStructuredFormatter(logging.Formatter):
    """
    Clase personalizada que modifica la forma en que se escriben los mensajes.
    En lugar de texto plano, transforma cada evento en un diccionario JSON organizado.
    """

    def format(self, record):
        """
        Función principal que toma un evento y lo convierte en el formato deseado.
        """

        # Construimos el diccionario con la información básica del evento
        log_record = {
            "timestamp": self.formatTime(
                record, self.datefmt
            ),  # Hora exacta del evento
            "level": record.levelname,  # Nivel de severidad (INFO, ERROR, etc.)
            "module": record.module,  # Nombre del archivo/módulo de origen
            "line": record.lineno,  # Número de línea donde ocurrió
            "message": record.getMessage(),  # El mensaje descriptivo del evento
        }

        # Verificamos si el evento contiene metadatos adicionales y los agregamos
        if hasattr(record, "data_meta"):
            log_record["metadata"] = record.data_meta

        # Retornamos el diccionario convertido a un texto JSON válido
        return json.dumps(log_record, ensure_ascii=False)


# ========================================================
# --- BLOQUE 3: CONFIGURACIÓN DEL REGISTRADOR (LOGGER) ---
# ========================================================


# 🛰️ Inicialización del Logger de Trazabilidad
def get_trazability_logger():
    """
    Función encargada de crear y configurar el "registrador" principal.
    Garantiza que el sistema esté listo para guardar nuestros mensajes.
    """

    # Obtenemos o creamos un logger con el nombre "E2E_Trace"
    logger = logging.getLogger("E2E_Trace")

    # Establecemos el nivel mínimo de importancia que vamos a registrar (INFO en adelante)
    logger.setLevel(logging.INFO)

    # Verificamos si el logger ya tiene salidas configuradas para evitar duplicarlas
    if not logger.handlers:
        # Creamos una salida para mostrar los logs en la consola (pantalla)
        console_handler = logging.StreamHandler()

        # Asociamos nuestro formato JSON a la salida de la consola
        formatter = JsonStructuredFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        # Agregamos esta configuración al logger principal
        logger.addHandler(console_handler)

    # Devolvemos el logger completamente configurado y listo para usarse
    return logger


# ======================================================
# --- BLOQUE 4: PUNTO DE ENTRADA Y PRUEBA DEL SCRIPT ---
# ======================================================

# Bloque de ejecución principal: se ejecuta solo si corremos el script directamente
if __name__ == "__main__":
    # Inicializamos nuestro motor de trazabilidad llamando a la función configurada
    log = get_trazability_logger()

    # Enviamos nuestro primer mensaje de prueba para confirmar que todo funciona
    log.info("Motor de trazabilidad inicializado correctamente.")
