"""
Título: Script de Validación de Integridad de Datos de Empleados

Objetivo: Verificar la calidad de datos críticos en la tabla 'employee_master_data'.

Descripción: Este script se conecta a una base de datos PostgreSQL para revisar si
existen valores nulos en columnas clave y detectar registros con salarios inválidos
(menores o iguales a cero), generando un reporte en consola.

Archivo Python: day03_integrity_audit.py

Archivo PNG: day03_integrity_audit.png
"""

# --- IMPORTACIÓN DE LIBRERÍAS ---
# 'pandas' para manipulación y análisis de datos.
import pandas as pd
# 'create_engine' para establecer la conexión con la base de datos SQL.
from sqlalchemy import create_engine
# 'os' para interactuar con el sistema operativo y leer variables de entorno.
import os
# 'load_dotenv' para cargar credenciales seguras desde un archivo .env.
from dotenv import load_dotenv

# --- CONFIGURACIÓN Y CONEXIÓN ---
# Carga las variables del archivo .env (usuario, contraseña, host, etc.)
load_dotenv()

# Crea la conexión a PostgreSQL utilizando las credenciales cargadas anteriormente.
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- DEFINICIÓN DE LA FUNCIÓN DE VALIDACIÓN ---
def check_integrity():
    """
    Función que ejecuta las consultas de validación de calidad de datos.
    """
    # 1. Lee la tabla 'employee_master_data' y la carga en un DataFrame de pandas.
    df = pd.read_sql("SELECT * FROM employee_master_data", con=engine)

    # 2. Define qué columnas deben tener datos obligatoriamente (no nulos).
    critical_cols = ['employee_number', 'monthly_income', 'department']

    # 3. Cuenta los valores nulos (vacíos) solo en esas columnas críticas.
    null_counts = df[critical_cols].isnull().sum()

    # 4. Imprime el reporte de nulos encontrado.
    print("📋 Reporte de Nulos:")
    print(null_counts)

    # 5. Busca registros donde el salario mensual sea inválido (0 o negativo).
    invalid_salaries = df[df['monthly_income'] <= 0]

    # 6. Comprueba si se encontraron salarios inválidos y muestra un mensaje de alerta.
    if not invalid_salaries.empty:
        print(f"⚠️ Alerta: Se encontraron {len(invalid_salaries)} registros con salario <= 0")
    else:
        print("✅ Calidad de salarios validada.")

# --- EJECUCIÓN DEL SCRIPT ---
# Asegura que la función se ejecute al correr el script directamente.
if __name__ == "__main__":
    check_integrity()