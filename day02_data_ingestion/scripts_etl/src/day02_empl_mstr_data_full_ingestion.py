# ==============================================================================
# Título: Pipeline de Ingesta de Datos de RRHH (IBM Attrition)
# 
# Objetivo: Automatizar la lectura, limpieza y carga de datos de recursos humanos
# desde un archivo CSV local hacia una base de datos PostgreSQL.
# 
# Descripción: Este script lee un dataset de rotación de empleados, estandariza 
# los nombres de las columnas a formato snake_case, limpia espacios en blanco y 
# carga la información en una tabla SQL para su análisis.
#
# Archivo Python: day02_empl_mstr_data_full_ingestion.py
#
# Archivo PNG: day02_empl_mstr_data_full_ingestion.png
# ==============================================================================

# --- Importación de herramientas (Librerías) ---
import pandas as pd              # Permite trabajar con tablas de datos de forma muy sencilla.
from sqlalchemy import create_engine  # Es el motor que nos permite "hablar" con la base de datos.
import os                        # Sirve para interactuar con las carpetas de tu computadora.
from dotenv import load_dotenv   # Ayuda a leer archivos secretos (.env) donde guardamos contraseñas.
from pathlib import Path         # Facilita la creación de rutas de archivos que funcionen en cualquier PC.
import re                        # Herramienta avanzada para buscar y reemplazar patrones en textos.

# ---------------------------------------------------------
# 1. Configuración de rutas y ubicación de archivos
# ---------------------------------------------------------

# Localiza la carpeta principal del proyecto subiendo tres niveles desde este archivo.
base_dir = Path(__file__).resolve().parents[3]

# Define la ruta exacta de la carpeta donde se guardan los datos originales de RRHH.
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'

# Guarda el nombre del archivo de IBM que vamos a procesar.
rrhh_file_name = 'WA_Fn-UseC_-HR-Employee-Attrition'

# Une la carpeta y el nombre del archivo para obtener la dirección completa en el disco.
rrhh_path_csv = os.path.join(target_raw_dir, f'{rrhh_file_name}.csv')

# ---------------------------------------------------------
# 2. Configuración de Conexión a Base de Datos
# ---------------------------------------------------------

try:
    # Carga las variables de seguridad (usuario, clave, servidor) desde el archivo .env.
    load_dotenv()
    
    # Construye la URL de conexión usando las credenciales guardadas en el sistema.
    DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    # Crea el enlace oficial (engine) para enviar la información a PostgreSQL.
    engine = create_engine(DB_URL)
except Exception as e:
    # Si la conexión falla (por ejemplo, clave incorrecta), muestra el error aquí.
    print(f"❌ Error al conectarse a PostgreSQL: {e}")

def run_pipeline():
    """Función principal que ejecuta los pasos de lectura, limpieza y carga."""
    try:
        # ---------------------------------------------------------
        # 3. Lectura de Datos (Extracción)
        # ---------------------------------------------------------
        print("🔍 Leyendo Dataset de IBM...")
        
        # Abre el archivo CSV y lo convierte en una tabla digital (DataFrame).
        df = pd.read_csv(rrhh_path_csv)

        # ---------------------------------------------------------
        # 4. Limpieza y Transformación (Formateo)
        # ---------------------------------------------------------
        print("🛠️ Limpiando y transformando datos...")
        
        # Función interna para convertir nombres tipo 'ColumnaEjemplo' a 'columna_ejemplo'.
        def to_snake_case(name):
            # Identifica letras mayúsculas pegadas a minúsculas para separarlas.
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            # Agrega guiones bajos, convierte todo a minúsculas y devuelve el nombre listo.
            return re.sub('([a-z0-0])([A-Z])', r'\1_\2', s1).lower()
        
        # Aplica el cambio de nombre a todas las columnas de la tabla al mismo tiempo.
        df.columns = [to_snake_case(col) for col in df.columns]
        
        # Ajusta manualmente un nombre específico para que sea más claro (over_18).
        df.rename(columns = {'over18' : 'over_18'}, inplace = True)
        
        # Revisa cada celda: si es texto, quita los espacios sobrantes a los lados.
        # Se usa .map porque .applymap está quedando obsoleto en versiones nuevas.
        df = df.map(lambda x : x.strip() if isinstance(x, str) else x)

        # ---------------------------------------------------------
        # 5. Carga de Datos (Destino final)
        # ---------------------------------------------------------
        print(f"📦 Cargando {len(df)} registros y {len(df.columns)} columnas...")
        
        # Envía la tabla a la base de datos en bloques de 500 filas para no saturar la conexión.
        # 'append' significa que agrega la información al final de la tabla existente.
        df.to_sql('employee_master_data', con = engine, if_exists = 'append', index = False, chunksize = 500)
        
        print("✅ Pipeline completado con éxito.")
        
    except Exception as e:
        # Si algo sale mal durante el proceso, imprime una cruz y la explicación técnica.
        print(f"❌ Error en pipeline: {e}")

# ---------------------------------------------------------
# 6. Ejecución del Script
# ---------------------------------------------------------

# Indica que el programa debe empezar a correr solo si abrimos este archivo directamente.
if __name__ == "__main__":
    run_pipeline()