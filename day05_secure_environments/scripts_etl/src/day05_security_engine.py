# ----------------------------------------------------------------------------------
# Título: Script de Validación de Conexión a PostgreSQL
# 
# Objetivo: Establecer y verificar una conexión segura a una base de datos PostgreSQL 
# utilizando SQLAlchemy.
# 
# Descripción: Este script lee credenciales desde un archivo local (.env) para evitar 
# exponer datos sensibles, configura el motor de conexión y realiza una prueba para 
# asegurar que la base de datos es accesible.
#
# Archivo Python: day05_secure_main_connection.py
# 
# Archivo PNG:  day05_secure_main_connection.png
# ----------------------------------------------------------------------------------

# --- BLOQUE 1: Importación de herramientas ---
# pandas: Nos servirá para manejar tablas de datos más adelante
import pandas as pd
# sqlalchemy: Es el "traductor" que permite a Python hablar con la base de datos
from sqlalchemy import create_engine
# os y dotenv: Se encargan de leer archivos de configuración secretos por seguridad
import os
from dotenv import load_dotenv

# --- BLOQUE 2: Configuración del Entorno ---
# Carga las variables de entorno desde un archivo .env (usuarios, passwords, etc.)
# Esto evita tener credenciales explícitas en el código.
load_dotenv()

# --- BLOQUE 3: Obtención de Credenciales y Validación ---
def get_secure_engine():
    """Recupera credenciales del sistema y verifica que estén completas."""
    # Lee cada credencial individual desde las variables de entorno
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    # Verifica que ninguna credencial esté vacía antes de intentar conectar
    if not all([db_user, db_pass, db_host, db_port, db_name]):
        raise ValueError("\n❌ Error: Faltan credenciales en el archivo .env")

    # --- BLOQUE 4: Creación del Motor (Engine) ---
    # Crea el motor de SQLAlchemy (engine), que maneja el pool de conexiones a la DB.
    # Construye la URL de conexión usando el formato: postgresql://user:pass@host:port/dbname
    engine = create_engine(
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    return engine

# --- BLOQUE 5: Inicialización y Prueba de Conexión ---
# Genera el motor de conexión llamando a la función definida anteriormente
engine = get_secure_engine()

def test_connection():
    """
    Intenta conectarse a la base de datos para verificar que el pipeline está listo para trabajar.
    """
    try:
        # Intenta abrir una conexión para confirmar que funciona
        with engine.connect() as conn:
            print("\n✅ Motor de base de datos inicializado con variables de entorno.")
            print("\n")
    except Exception as e:
        # Si ocurre un error, imprime el mensaje para diagnosticar el fallo
        print(f"\n❌ Error de Conexión: {e}")
        print("\n")

# --- BLOQUE 6: Ejecución Principal ---
if __name__ == "__main__":
    # Llama a la función de prueba solo si el script se ejecuta directamente.
    test_connection()