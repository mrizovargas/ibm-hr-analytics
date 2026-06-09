# ----------------------------------------------------------------------------------
# Título: Auditoría de Variables de Entorno para Base de Datos
#
# Objetivo: Validar que el entorno local contenga todas las credenciales y datos de
# configuración críticos antes de intentar conectar a una base de datos.
#
# Descripción: Este script carga un archivo de configuración y verifica que las
# variables de entorno necesarias para la conexión (usuario, contraseña, servidor,
# puerto y nombre de la base de datos) existan. Si falta alguna, detiene el proceso
# y alerta al usuario para evitar errores futuros.
#
# Archivo Python: security_engine.py
# ----------------------------------------------------------------------------------

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
# pandas: Nos servirá para manejar tablas de datos más adelante
import pandas as pd

# sqlalchemy: Es el "traductor" que permite a Python hablar con la base de datos
from sqlalchemy import create_engine

# os y dotenv: Se encargan de leer archivos de configuración secretos por seguridad
import os
from dotenv import load_dotenv

# Permite mostrar y registrar mensajes informativos en la consola sobre el avance del script
import logging

# ==========================================
# --- BLOQUE 2: CONFIGURACIÓN Y CONEXIÓN ---
# ==========================================
# Carga las variables de entorno desde un archivo .env (usuarios, passwords, etc.)
# Esto evita tener credenciales explícitas en el código.
load_dotenv()

# Configura el formato de los mensajes en consola, añadiendo la hora exacta, el tipo de mensaje y su contenido
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ========================================================
# --- BLOQUE 3: OBTENCIÓN DE CREDENCIALES Y VALIDACIÓN ---
# ========================================================
def get_secure_engine():
    """
    Crea un motor de base de datos SQL seguro utilizando variables de entorno.

    Esta función lee las credenciales del sistema para conectarse a la base de datos
    donde está alojado el dataset 'IBM HR Analytics Employee Attrition & Performance'.

    Variables de Entorno Requeridas:
        DB_USER (str): Usuario de la base de datos (ej. 'admin').
        DB_PASS (str): Contraseña del usuario.
        DB_HOST (str): Dirección del servidor (ej. '192.168.1.10').
        DB_PORT (str): Puerto (ej. '5432').
        DB_NAME (str): Base de datos (ej. 'human_resources').

    Returns:
        sqlalchemy.engine.base.Engine: Motor de conexión de SQLAlchemy.

    Raises:
        ValueError: Si alguna variable de entorno necesaria no está configurada.
    """

    # Lee cada credencial individual desde las variables de entorno
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Lista de llaves obligatorias (nombres de las variables a buscar)
    required_keys = ["DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]

    # Bucle para recorrer cada llave obligatoria
    for key in required_keys:
        # Evalúa si la variable no existe o está vacía en el entorno
        if not os.getenv(key):
            # Imprime encabezado de alerta
            logging.info("====== AUDITORIA DE SEGURIDAD ======")
            # Informa exactamente qué variable hace falta para corregirlo
            logging.info(f"❌ Falta la variable de entorno: {key}")
            print("\n")
            # Retorna Falso indicando que la auditoría falló
            return False

    # =============================================
    # --- BLOQUE 4: CREACIÓN DEL MOTOR (engine) ---
    # =============================================
    # Crea el motor de SQLAlchemy (engine), que maneja el pool de conexiones a la DB.
    # Construye la URL de conexión usando el formato: postgresql://user:pass@host:port/dbname
    try:
        # Crea el motor de SQLAlchemy (engine), que maneja el pool de conexiones a la DB.
        # Construye la URL de conexión usando el formato: postgresql://user:pass@host:port/dbname
        engine = create_engine(
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )

        # Retornar motor (Qué hace: inicializa el objeto)
        return engine

    except Exception as e:
        # Si la conexión falla (por ejemplo, clave incorrecta), muestra el error aquí.
        logging.info(f"❌ Error al conectarse a PostgreSQL: {e}")
        print("\n")

    # Si pasa el bucle sin problemas, imprime encabezado de éxito
    logging.info("====== AUDITORIA DE SEGURIDAD ======")
    # Confirma que todo está correcto
    logging.info("✅ Todas las variables críticas están presentes.")


# =====================================================
# --- BLOQUE 5: INICIALIZACIÓN Y PRUEBA DE CONEXIÓN ---
# =====================================================
# Genera el motor de conexión llamando a la función definida anteriormente

engine = get_secure_engine()


def test_connection():
    """
    Intenta conectarse a la base de datos para verificar que el pipeline está listo para trabajar.
    """
    try:
        # Intenta abrir una conexión para confirmar que funciona
        with engine.connect() as conn:
            logging.info(
                "✅ Motor de base de datos inicializado con variables de entorno."
            )
    except Exception as e:
        # Si ocurre un error, imprime el mensaje para diagnosticar el fallo
        logging.info(f"❌ Error de Conexión: {e}")
        print("\n")


# ======================================
# --- BLOQUE 6: EJECUCIÓN DEL SCRIPT ---
# ======================================
if __name__ == "__main__":
    # Llama a la función de prueba solo si el script se ejecuta directamente.
    test_connection()
