# ==============================================================================
# Título: Pipeline de Verificación de Conexión a PostgreSQL
# 
# Objetivo: Validar que el pipeline de datos pueda conectarse correctamente a la 
# base de datos PostgreSQL antes de iniciar procesos pesados.
# 
# Descripción: Este script lee credenciales seguras, establece un motor de 
# conexión, y ejecuta una prueba de ping para confirmar la conectividad.
#
# Archivo Python: day01_main_connection.py
# ==============================================================================

# --- BLOQUE 1: Importación de herramientas ---
# Pandas nos servirá para manejar tablas de datos más adelante
import pandas as pd 

# SQLAlchemy es el "traductor" que permite a Python hablar con la base de datos
from sqlalchemy import create_engine 

# OS y Dotenv se encargan de leer archivos de configuración secretos por seguridad
import os 
from dotenv import load_dotenv 

# --- BLOQUE 2: Configuración del Entorno ---
# Carga las variables de entorno desde un archivo .env (usuarios, passwords, etc.)
# Esto evita tener credenciales explícitas en el código.
load_dotenv()

# --- BLOQUE 3: Definición de la Conexión ---
# Construye la URL de conexión usando el formato: postgresql://user:pass@host:port/dbname
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Crea el motor de SQLAlchemy (engine), que maneja el pool de conexiones a la DB.
engine = create_engine(DB_URL)

# --- BLOQUE 4: Función de Prueba de Conexión ---
def test_connection():
    """
    Intenta conectarse a la base de datos para verificar que el
    pipeline está listo para trabajar.
    """
    try:
        # Intenta abrir una conexión para confirmar que funciona
        with engine.connect() as conn:
            print("✅ Conexión Exitosa a Postgres - Pipeline Activo")
    except Exception as e:
        # Si ocurre un error, imprime el mensaje para diagnosticar el fallo
        print(f"❌ Error de Conexión: {e}")

# --- BLOQUE 5: Ejecución Principal ---
if __name__ == "__main__":
    # Llama a la función de prueba solo si el script se ejecuta directamente.
    test_connection()