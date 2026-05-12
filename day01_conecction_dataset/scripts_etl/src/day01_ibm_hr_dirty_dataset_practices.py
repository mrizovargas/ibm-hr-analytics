# ---------------------------------------------------------------------
# Título: Generador de Datos Sucios - Dataset IBM HR
# 
# Objetivo: Simular un escenario de datos reales "sucios" para prácticas 
# de Data Cleaning.
# 
# Descripción: El script toma el dataset original de recursos humanos de 
# IBM y introduce artificialmente nulos, inconsistencias de texto, valores 
# atípicos (outliers) y errores lógicos de negocio. Esto permite entrenar 
# procesos de limpieza y transformación.
# 
# Archivo Python: 
# 
# Archivo PNG: 
# ---------------------------------------------------------------------

# --- Importación de librerías ---

# pandas: Fundamental para la manipulación y análisis de datos en estructuras tipo tabla (DataFrames).
import pandas as pd
# numpy: Se utiliza para operaciones numéricas eficientes y manejo de valores nulos (NaN).
import numpy as np
# random: Librería estándar para generar aleatoriedad, útil para introducir errores o muestrear datos.
import random
# os y pathlib: Módulos para gestionar rutas de archivos y directorios de forma segura entre diferentes sistemas operativos.
import os
from pathlib import Path
# re: Permite utilizar expresiones regulares para buscar, limpiar o manipular texto complejo.
import re



# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS
# ---------------------------------------------------------

# --- Configuración de rutas del proyecto ---
# Localiza la carpeta raíz subiendo tres niveles y define las rutas de entrada (raw)
# y salida (raw) para mantener los datos organizados.
base_dir = Path(__file__).resolve().parents[3]
target_raw_dir = base_dir / '02_data' / 'raw' / 'rrhh'

# --- Identificación del archivo de origen ---
# Define el nombre específico del archivo de RRHH y construye su ruta 
# completa para que el sistema pueda localizarlo.
rrhh_file_name = 'WA_Fn-UseC_-HR-Employee-Attrition'
# Une la carpeta base de datos con el nombre del archivo y la extensión .csv
rrhh_path_csv = os.path.join(target_raw_dir, f'{rrhh_file_name}.csv')

# --- Generación del archivo de salida ---
# Crea un nombre único para el archivo procesado.
# Esto evita que los resultados nuevos sobrescriban a los anteriores.
raw_file_name = f'IBM_HR_Dirty_Practices.csv'
# Combina la ruta de destino con el nuevo nombre para definir dónde se guardará
path_csv = os.path.join(target_raw_dir, raw_file_name)


# ---------------------------------------------------------
# 2. NORMALIZACIÓN DE NOMBRES DE COLUMNAS
# ---------------------------------------------------------

# Convierte un texto de formato CamelCase o PascalCase a snake_case.
# Ejemplo: 'MiVariable' -> 'mi_variable'
def to_snake_case(name):
    # --- Bloque 1: Separar uniones entre minúsculas y mayúsculas ---
    # Busca una letra minúscula seguida de una mayúscula (CamelCase) y coloca un guion bajo.
    # Ejemplo: 'nombreUsuario' -> 'nombre_Usuario'
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)

    # --- Bloque 2: Separar acrónimos y convertir a minúsculas ---
    # Busca una letra o número minúsculo seguido de una mayúscula y coloca un guion bajo.
    # Luego, convierte todo el texto a minúsculas.
    # Ejemplo: 'nombre_Usuario' -> 'nombre_usuario'
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# ---------------------------------------------------------
# 3. CARGA DEL DATASET
# ---------------------------------------------------------
try:
    # --- Carga y normalización de datos ---
    # 1. Lee el archivo CSV especificado por 'rrhh_path_csv' y lo carga en la memoria como un DataFrame (tabla) de Pandas.
    df = pd.read_csv(rrhh_path_csv)
    
    # 2. Renombra las columnas: recorre cada columna ('col'), aplica una función 'to_snake_case' (probablemente definida antes) 
    #    para estandarizar el texto (ej: "Nombre Empleado" a "nombre_empleado") y sobrescribe los nombres originales.
    df.columns = [to_snake_case(col) for col in df.columns]

    # --- Preparación para la exportación ---
    # 3. Convierte el DataFrame de Pandas en una lista de diccionarios, donde cada diccionario representa una fila 
    #    (clave=columna, valor=dato), formato ideal para exportar a JSON o insertar en BD.
    datos_dict = df.to_dict(orient='records')
    
    # 4. Crea una lista con los nombres de las columnas limpias (snake_case) para usarlas como cabeceras al escribir el nuevo archivo.
    mis_cabeceras = df.columns.tolist()

except Exception as e:
    # 5. Si ocurre algún error (archivo no encontrado, formato incorrecto), captura la excepción y muestra un mensaje amigable 
    #    con el error técnico ('e') para saber qué falló sin detener el programa abruptamente.
    print(f"❌ Error al cargar o procesar el dataset: {e}")
    
    # 6. Inicializa 'datos_dict' como 'None' para indicar que la carga falló y evitar errores en el resto del script.
    datos_dict = None


# ---------------------------------------------------------
# 4. ANOMALÍAS ESTRUCTURALES (Nulos e Inconsistencias)
# ---------------------------------------------------------

# OBJETIVO: Generar datos sucios (nulos y errores de formato) para simulaciones.

# --- Bloque 1: Inyección de nulos (NaN) ---
# Se introduce un 5% de valores faltantes en 'MonthlyIncome' para simular 
# falta de información en ingresos.
df['monthly_income'] = df['monthly_income'].apply(
    # Para cada valor, genera un número aleatorio < 0.05 (5% prob) para poner NaN.
    lambda x: np.nan if random.random() < 0.05 else x
)

# Se introduce un 3% de valores faltantes en 'TotalWorkingYears' para simular 
# errores en el historial laboral.
df['total_working_years'] = df['total_working_years'].apply(
    # Para cada valor, genera un número aleatorio < 0.03 (3% prob) para poner NaN.
    lambda x: np.nan if random.random() < 0.03 else x
)

# --- Bloque 2: Inconsistencias de formato/texto ---
# Creamos una lista de errores comunes de entrada de datos para el departamento "Sales".
choices = ['sales', 'SALES', 'Sales ', 'S_ales']

# Buscamos la columna 'Department' y modificamos solo los registros que dicen "Sales".
df['department'] = df['department'].apply(
    # Si el valor es exacto a 'Sales', elige al azar un formato erróneo de la lista 'choices'.
    lambda x: random.choice(choices) if x == 'Sales' else x
)

# Introduce espacios en blanco al final de cualquier departamento aleatoriamente
df['department'] = df['department'].apply(lambda x: f"{x} " if random.random() < 0.1 else x)

# ---------------------------------------
# 5. ANOMALÍAS DE CALIDAD (Outliers)
# ---------------------------------------

# OBJETIVO: Introducir valores numéricos extremos (outliers) no lógicos en la
# columna 'MonthlyIncome' para simular errores de datos o casos excepcionales.


# --- Paso 1: Identificar filas para salarios astronómicos (Outliers superiores) ---
# Seleccionamos al azar 15 índices (filas) del DataFrame para aumentar su salario.
indices_outliers_altos = df.sample(n=15).index
# Multiplicamos por 15 los salarios de los índices seleccionados (Outliers superiores)
df.loc[indices_outliers_altos, 'monthly_income'] = df.loc[indices_outliers_altos, 'monthly_income'] * 15

# --- Paso 2: Identificar filas para salarios simbólicos (Outliers inferiores) ---
# Seleccionamos al azar 10 índices (filas) diferentes para asignarles un salario de 1.
indices_outliers_bajos = df.sample(n=10).index
# Asignamos 1 a los índices de salarios simbólicos (Outliers inferiores)
df.loc[indices_outliers_bajos, 'monthly_income'] = 1


# --------------------------------------
# 6. ANOMALÍAS DE LÓGICA DE NEGOCIO
# --------------------------------------

# Objetivo: Crear datos que son físicamente imposibles o contradictorios (ruido)
# para probar la robustez de algoritmos de limpieza o modelos de ML.

# --- Bloque 1: Generar error de lógica temporal (Antigüedad > Edad) ---
# Selecciona aleatoriamente 18 índices (filas) del DataFrame para aplicar el error.
idx_antiguedad = df.sample(n=18).index

# Modifica 'YearsAtCompany' (Años en la empresa):
# Para las filas seleccionadas, establece la antigüedad como Edad + 10.
# Esto genera un error físico: nadie puede trabajar más años de los que tiene de vida.
df.loc[idx_antiguedad, 'years_at_company'] = df.loc[idx_antiguedad, 'age'] + 10

# --- Bloque 2: Generar error de secuencia lógica (Promoción > Antigüedad) ---
# Selecciona 8 empleados al azar para alterar sus datos de promoción.
idx_promocion = df.sample(n=8).index

# Modifica 'YearsSinceLastPromotion' (Años desde la última promoción):
# Asigna la antigüedad actual + 5 años.
# Error: La promoción es anterior o más antigua que el tiempo que llevan en la empresa.
df.loc[idx_promocion, 'years_since_last_promotion'] = df.loc[idx_promocion, 'years_at_company'] + 5

# --- Bloque 3: Generar error de datos faltantes/inválidos (Tarifa = 0) ---
# Selecciona 12 empleados al azar para poner su tarifa diaria en cero.
idx_tarifa = df.sample(n=12).index

# Modifica 'DailyRate' (Tarifa diaria):
# Asigna 0 a la tarifa diaria para los empleados seleccionados.
# Error: Un empleado no puede tener una tarifa diaria de cero (incoherencia económica).
df.loc[idx_tarifa, 'daily_rate'] = 0

# ---------------------------------------------
# 7. ANOMALÍAS DE LÓGICA SALARIAL AVANZADA ---
# ---------------------------------------------

# Objetivo: Crear escenarios complejos que requieren validaciones cruzadas.
# Se introducen anomalías intencionales en los datos para probar la detección de errores.

# --- 1. Definición de índices para las anomalías (Selección aleatoria) ---

# Selecciona 9 registros al azar para asignarles un valor negativo (simulando errores de sistema).
idx_negativos = df.sample(n=9).index
# Salarios Negativos -> Multiplica el salario actual por -1.
df.loc[idx_negativos, 'monthly_income'] = df.loc[idx_negativos, 'monthly_income'] * -1

# Selecciona 13 empleados de nivel 1 (Junior) para generar inconsistencias.
idx_desajuste = df[df['job_level'] == 1].sample(n=13).index
# Salarios Altos Inconsistentes -> Asigna un salario alto (25000),
# con solo 1 año en la empresa y 1 año de experiencia total.
df.loc[idx_desajuste, 'monthly_income'] = 25000
df.loc[idx_desajuste, 'years_at_company'] = 1
df.loc[idx_desajuste, 'total_working_years'] = 1

# Selecciona 8 empleados al azar para alterar sus datos de antigüedad y promoción.
idx_inconsistente = df.sample(n=8).index
# Inconsistencia lógica -> Fuerza a que el tiempo de promoción 
# sea superior a la antigüedad total en la empresa (ej. 20 años sin promover vs 2 años en empresa).
df.loc[idx_inconsistente, 'years_since_last_promotion'] = 20
df.loc[idx_inconsistente, 'years_at_company'] = 2

# ---------------------------------------------------------
# 8. Exportación de Datos.
# ---------------------------------------------------------

# Gestiona la creación de carpetas y guarda los datos procesados en un archivo CSV.
def exportar_a_csv(ruta_destino, datos, cabeceras):
    # 1. Validación inicial: Si no hay datos, cancelamos la función para evitar errores.
    if datos is None:
        return
    
    # 2. Manejo de excepciones: Captura errores (como archivos abiertos o permisos) sin detener el programa.
    try:
        # --- Preparación del entorno ---
        # Extraemos la carpeta contenedora de la ruta completa para verificarla.
        carpeta_destino = os.path.dirname(ruta_destino)
        
        # Si la carpeta no existe, la crea automáticamente (incluso carpetas anidadas).
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino, exist_ok=True)
            print(f'✅ Carpeta creada en: {carpeta_destino}')

        # --- Escritura del archivo ---
        # Abre el archivo en modo escritura ('w').
        # 'utf-8-sig' asegura que Excel lea bien tildes y eñes.
        # 'newline=''' evita líneas en blanco extra entre filas.
        with open(ruta_destino, mode='w', newline='', encoding='utf-8-sig') as archivo_csv:
            # Convierte el DataFrame de pandas a formato CSV.
            # sep='|' usa tubería como separador.
            # index=False evita guardar la columna de números de fila.
            datos.to_csv(archivo_csv, sep=',', index=False)

        # --- Confirmación y resumen ---
        # Muestra en consola un resumen técnico (columnas, tipos de datos, memoria).
        print(datos.info())
        print(f"\n✅ Proceso completado exitosamente.")
        print(f"📂 Archivo guardado en: {ruta_destino}")
        
    except PermissionError:
        # Error específico: Ocurre si el archivo está abierto en Excel u otro programa.
        print(f"❌ Error de Permiso: El archivo '{ruta_destino}' está abierto en otro programa.")
    except Exception as e:
        # Captura cualquier otro imprevisto durante la exportación.
        print(f"❌ Ocurrió un error inesperado al exportar: {e}")

# ---------------------------------------------------------
# 9. Punto de entrada del script.
# ---------------------------------------------------------

# Asegura que el proceso de limpieza y exportación solo se inicie si el 
# archivo se ejecuta directamente (no si se importa desde otro script).
if __name__ == "__main__":
    # Muestra un mensaje en consola para indicar que el script ha comenzado.
    print("--- Iniciando proceso de normalización ---\n")
    
    # Llama a la función principal para guardar los datos procesados en un archivo CSV,
    # pasando la ruta del archivo, el diccionario de datos y los nombres de las columnas.
    exportar_a_csv(path_csv, df, mis_cabeceras)