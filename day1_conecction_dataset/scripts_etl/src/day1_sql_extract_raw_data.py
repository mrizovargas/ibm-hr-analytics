"""
TÍTULO: Extracción Modular de Datos desde PostgreSQL
OBJETIVO: Consultar la tabla maestra de empleados de forma segura y organizada.
DESCRIPCIÓN: El script utiliza variables de entorno para proteger las credenciales,
se conecta a la base de datos 'ibm_hr', extrae una muestra de empleados y 
gestiona automáticamente el cierre de la conexión para optimizar recursos.
"""

import os
import psycopg2  # Conector para comunicarse con PostgreSQL
import pandas as pd  # Herramienta para analizar y organizar datos en tablas
from dotenv import load_dotenv  # Carga variables secretas desde un archivo .env

# Bloque de Configuración: Cargamos las credenciales ocultas del sistema
load_dotenv()

def obtener_conexion_db():
    """
    Establece el puente de comunicación con el servidor.
    Usa 'os.getenv' para leer los datos de acceso sin exponerlos en el código.
    """
    return psycopg2.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )

# Definimos cuántos registros queremos traer por defecto
limite = 10

def extraer_datos_empleados(limite):
    """
    Lógica principal para realizar la consulta y traer los datos a Python.
    """
    conn = None
    try:
        # Iniciamos la conexión llamando a la función anterior
        conn = obtener_conexion_db()
        
        # Definimos la instrucción SQL usando el límite solicitado
        query = f"""
        SELECT *
        FROM employee_master_data
        LIMIT {limite}
        """
        print("\n🚀 Iniciando ingesta PostgreSQL...")
    
        # pandas ejecuta la consulta y transforma el resultado en una tabla (DataFrame)
        df = pd.read_sql(query, conn)

        print("✅ ¡Datos cargados exitosamente!")
        return df

    except Exception as e:
        # Si algo falla (servidor caído, error de red), mostramos el motivo exacto
        print(f"❌ Error al conectar o procesar la base de datos: {e}")
        return None

    finally:
        # Bloque de Cierre: Pase lo que pase, nos aseguramos de cerrar la conexión
        if conn:
            conn.close()

# Bloque de Ejecución: Punto de partida del programa
if __name__ == "__main__":
    # Llamamos a la función principal usando el límite definido arriba
    df_empleados = extraer_datos_empleados(limite)
    
    # Si la descarga fue exitosa, mostramos los resultados en pantalla
    if df_empleados is not None:
        print("\n Vista previa de los datos:")
        print(df_empleados.head())