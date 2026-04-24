"""
TÍTULO: Pipeline de Normalización y Limpieza de Datos de RRHH
OBJETIVO: Automatizar la lectura de reportes de Recursos Humanos, estandarizar los 
nombres de las columnas a formato 'snake_case' y exportar una versión limpia con 
marca de tiempo, asegurando la compatibilidad con Excel y el orden histórico.
"""

# Herramientas para el manejo de datos y archivos CSV
import pandas as pd 
import csv 

# Utilidades para interactuar con las carpetas y rutas del sistema operativo
import os 
from pathlib import Path 

# Funciones para limpieza de texto (expresiones regulares) y gestión de fechas
import re 
from datetime import datetime 


# ---------------------------------------------------------
# 1. Configuración de rutas.
# ---------------------------------------------------------

# --- Configuración de rutas del proyecto ---
# Localiza la carpeta raíz subiendo tres niveles y define las rutas de entrada (raw)
# y salida (processed) para mantener los datos organizados.
base_dir = Path(__file__).resolve().parents[2]
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'
cleaned_target_dir = base_dir / '02_data' / 'processed' / 'rrhh'

# --- Identificación del archivo de origen ---
# Define el nombre específico del archivo de RRHH y construye su ruta 
# completa para que el sistema pueda localizarlo.
rrhh_file_name = 'WA_Fn-UseC_-HR-Employee-Attrition'
rrhh_path_csv = os.path.join(target_raw_dir, f'{rrhh_file_name}.csv')

# --- Generación del archivo de salida con marca de tiempo ---
# Crea un nombre único para el archivo procesado usando la fecha y hora actual.
# Esto evita que los resultados nuevos sobrescriban a los anteriores.
time_stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
cleaned_file_name = f'rrhh_limpio_{time_stamp}.csv'
path_csv = os.path.join(cleaned_target_dir, cleaned_file_name)


# ---------------------------------------------------------
# 2. Normalización de Nombres de Columnas.
# ---------------------------------------------------------
def to_snake_case(name):
    """
    Convierte un texto de formato CamelCase o PascalCase a snake_case.
    """
    # Inserta un guion bajo entre una letra minúscula y una mayúscula que inicia una palabra.
    # Ejemplo: "EmpleadoId" -> "Empleado_Id"
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)

    # Maneja casos con números o mayúsculas consecutivas y convierte todo a minúsculas.
    # Ejemplo: "Empleado_Id" -> "empleado_id"
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# ---------------------------------------------------------
# 3. Carga del Datset.
# ---------------------------------------------------------
try:
    # --- Carga y normalización de datos ---
    # Importamos el archivo CSV a un formato de tabla (DataFrame) y transformamos 
    # todos los nombres de las columnas a 'snake_case' para estandarizar el formato.
    df = pd.read_csv(rrhh_path_csv)
    df.columns = [to_snake_case(col) for col in df.columns]

    # --- Preparación para la exportación ---
    # Convertimos la tabla en una lista de diccionarios y extraemos los nombres 
    # de las columnas; esto facilita la escritura posterior del archivo limpio.
    datos_dict = df.to_dict(orient='records')
    mis_cabeceras = df.columns.tolist()

except Exception as e:
    # Gestión de errores en caso de que el archivo no exista o el formato sea incorrecto.
    print(f"❌ Error al cargar o procesar el dataset: {e}")
    datos_dict = None


# ---------------------------------------------------------
# 4. Exportación de Datos.
# ---------------------------------------------------------
def exportar_a_csv(ruta_destino, datos, cabeceras):
    """
    Gestiona la creación de carpetas y guarda los datos procesados en un archivo CSV.
    """
    if datos is None:
        return
    
    try:
        # --- Preparación del entorno ---
        # Verifica si existe la carpeta de destino; si no, la crea automáticamente
        # para evitar errores al intentar guardar el archivo.
        if not os.path.exists(cleaned_target_dir):
            os.makedirs(cleaned_target_dir, exist_ok=True)
            print(f'✅ Carpeta creada en: {cleaned_target_dir}')

        # --- Escritura del archivo ---
        # Abre el archivo con codificación 'utf-8-sig' para que Excel reconozca 
        # correctamente tildes y eñes. Se usa el delimitador '|' para mayor claridad.
        with open(ruta_destino, mode='w', newline='', encoding='utf-8-sig') as archivo_csv:
            df.to_csv(archivo_csv, sep='|', index=False)

        # --- Confirmación y resumen ---
        # Muestra en consola un resumen técnico de los datos guardados y 
        # confirma la ubicación final del archivo.
        print(df.info())
        print(f"\n✅ Proceso completado exitosamente.")
        print(f"📂 Archivo guardado en: {ruta_destino}")
        print(f"📄 CSV: {cleaned_file_name}")
        
    except PermissionError:
        # Error común si el archivo de destino está abierto en Excel o por otro usuario.
        print(f"❌ Error de Permiso: El archivo '{ruta_destino}' está abierto en otro programa.")
    except Exception as e:
        # Captura cualquier otro imprevisto durante la exportación.
        print(f"❌ Ocurrió un error inesperado al exportar: {e}")

# --- Punto de entrada del script ---
# Asegura que el proceso de limpieza y exportación solo se inicie si el 
# archivo se ejecuta directamente (no si se importa desde otro script).
if __name__ == "__main__":
    print("--- Iniciando proceso de normalización ---\n")
    exportar_a_csv(path_csv, datos_dict, mis_cabeceras)