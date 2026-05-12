"""
Título: Auditoría de Tipos de Datos en PostgreSQL

Objetivo: Validar que columnas específicas de una tabla en la base de datos
se estén leyendo con el tipo de dato correcto (entero) en Python.

Descripción: Este script se conecta a una base de datos PostgreSQL, lee
una muestra de la tabla 'employee_master_data' y utiliza pandas para 
verificar si las columnas de edad, ingresos y número de empleado son 
tratadas como números enteros, evitando problemas de texto inesperado.

Archivo Phyton: day03_test_types.py

Archivo PNG: day03_test_types.png
"""

# --- IMPORTACIÓN DE LIBRERÍAS ---
import pandas as pd                     # Librería para manipulación y análisis de datos
from sqlalchemy import create_engine    # Módulo para conectar con la base de datos
import os                               # Librería para acceder a variables de entorno
from dotenv import load_dotenv          # Módulo para cargar configuraciones desde un archivo .env

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Carga las variables de entorno (usuario, pass, host, etc.) desde el archivo .env
load_dotenv()

# Crea el motor de conexión a PostgreSQL usando las credenciales seguras
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- DEFINICIÓN DE LA FUNCIÓN DE VALIDACIÓN ---
def validate_db_structure():
    """
    Lee una muestra de datos y valida que las columnas seleccionadas
    sean de tipo entero.
    """
    # 1. Lee la primera fila de la tabla para analizar la estructura rápidamente
    df = pd.read_sql("SELECT * FROM employee_master_data LIMIT 1", con=engine)
    
    # 2. Imprime los tipos de datos actuales que detecta Pandas
    print("--- Auditoría de Tipos de Datos (Panda) ---")
    print(df[['age', 'monthly_income', 'employee_number']].dtypes)
    print("-" * 40)

    # 3. Validaciones bloque por bloque (Línea por línea)
    
    # Valida columna 'age'
    if pd.api.types.is_integer_dtype(df['age']):
        print("✅ Validación exitosa: 'age' es un entero puro.")
    else:
        print("❌ Error: La columna 'age' se lee como objeto/texto.")

    # Valida columna 'monthly_income'
    if pd.api.types.is_integer_dtype(df['monthly_income']):
        print("✅ Validación exitosa: 'monthly_income' es un entero puro.")
    else:
        print("❌ Error: La columna 'monthly_income' se lee como objeto/texto.")

    # Valida columna 'employee_number'
    if pd.api.types.is_integer_dtype(df['employee_number']):
        print("✅ Validación exitosa: 'employee_number' es un entero puro.")
    else:
        print("❌ Error: La columna 'employee_number' se lee como objeto/texto.")

# --- EJECUCIÓN PRINCIPAL ---
# Punto de entrada del script
if __name__ == "__main__":
    validate_db_structure()