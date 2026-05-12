"""
Título: Pipeline de Auditoría de Integridad de Datos

Objetivo: Validar la correcta inserción y lectura de datos específicos en la base de 
datos PostgreSQL.

Descripción: Este script verifica si un registro de prueba (empleado 9999) existe y 
si su salario mensual coincide con el valor esperado, asegurando la integridad del 
flujo de datos.

Archivo Python: day01_empl_mstr_data_audit.py

Archivo PNG: day01_empl_mstr_data_audit.png
"""

import pandas as pd # Biblioteca para manipular los datos en tablas (DataFrames)
from sqlalchemy import create_engine # Módulo para conectar con la base de datos
import os # Para leer variables de entorno del sistema
from dotenv import load_dotenv # Para cargar configuraciones secretas (.env)

# --- CONFIGURACIÓN DE ENTORNO Y BASE DE DATOS ---
# Carga las variables de entorno desde el archivo .env para proteger credenciales
load_dotenv()

# Construye la URL de conexión a PostgreSQL usando variables de entorno
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Crea el motor de conexión para interactuar con la base de datos
engine = create_engine(DATABASE_URL)

def run_audit():
    """Ejecuta la auditoría buscando el registro 9999."""
    print("--- Iniciando Auditoría de Conexión ---")

    # Define la consulta SQL para extraer datos del empleado de prueba
    query = """
    SELECT employee_number, age, department, monthly_income
    FROM employee_master_data
    WHERE employee_number = 9999;
    """

    try:
        # --- BLOQUE DE AUDITORÍA ---
        # Ejecuta la consulta y carga los resultados en un DataFrame de pandas
        df = pd.read_sql(query, con=engine)

        # Verifica si el DataFrame no está vacío
        if not df.empty:
            print("✅ Registro de prueba detectado con éxito:")
            print(df)
            
            # Valida si el salario mensual (monthly_income) es el esperado (99999)
            if df['monthly_income'][0] == 99999:
                print("✅ Integridad de datos: Confirmada")
            else:
                print("⚠️ Valor de datos incorrecto en el registro 9999.")
        else:
            # Indica si la consulta funcionó pero no encontró el registro
            print("⚠️ No se encontró el registro 9999. Revisa la inserción en SQL.")

    except Exception as e:
        # Captura y muestra errores de conexión o ejecución
        print(f"❌ Error crítico en pipeline: {e}")

if __name__ == "__main__":
    # Ejecuta la función de auditoría
    run_audit()