# =============================================================================
# Título: Simulación de Desacoplamiento de Capas (Layer Decoupling) en Python
#
# Objetivo: Demostrar cómo una capa intermedia protege los reportes de cambios
# en la BD.
#
# Descripción: Este script emula en Python el flujo de ingeniería de datos que
# realizamos con las vistas de SQL. Simula un escenario donde el equipo de TI
# renombra una columna clave en la base de datos central. El programa demuestra
# cómo aplicar un "contrato de mapeo" intermedio para absorber la modificación,
# garantizando que las herramientas de BI / Tableau sigan recibiendo sus datos con la
# estructura original sin enterarse del cambio de infraestructura.
#
# Archivo Python: day13_sim_layer_decoupling.py
#
# Archivo PNG: day13_layer_decoupling_architecture.png
# =============================================================================

# =============================================================================
# BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS
# Objetivo: Cargar las herramientas básicas para manipular los datos.
# =============================================================================
# Importamos pandas, la librería estándar para manejar tablas de datos.
import pandas as pd

# =============================================================================
# BLOQUE 2: ESTADO INICIAL (Antes de la migración de TI)
# Objetivo: Replicar la estructura original de la base de datos corporativa.
# =============================================================================
# Diccionario que simula los registros originales de Recursos Humanos.
data_origen = {
    "employee_number": [1, 2, 3],
    # Nombre original de la columna de costos antes del cambio de TI.
    "daily_rate": [1102, 279, 1373],
    "attrition": ["Yes", "No", "Yes"],
}

# Convertimos el diccionario en un DataFrame (una tabla estructurada).
df_nucleo_bd_antiguo = pd.DataFrame(data_origen)

# Creamos la vista inicial que Power BI o Tableau consumen de manera regular.
vista_para_powerbi_inicial = df_nucleo_bd_antiguo[["employee_number", "daily_rate"]]

# Mostramos una vista previa del estado inicial para comprobar los nombres.
print("\nVista inicial entregada a Power BI (Sin cambios):")
print(vista_para_powerbi_inicial.head(1))
print("-" * 50)


# =============================================================================
# BLOQUE 3: MIGRACIÓN DEL NÚCLEO POR PARTE DE TI
# Objetivo: Simular el cambio físico de infraestructura en la tabla maestra.
# =============================================================================

# TI renombra la columna 'daily_rate' por 'costo_diario_operativo'.
df_nucleo_bd_nuevo = df_nucleo_bd_antiguo.rename(
    columns={"daily_rate": "costo_diario_operativo"}
)


# =============================================================================
# BLOQUE 4: DESACOPLAMIENTO ESTRUCTURAL (Layer Decoupling)
# Objetivo: Traducir el nuevo esquema técnico al formato esperado por el BI.
# =============================================================================

# Definimos un diccionario de mapeo que actúa como contrato de traducción.
contrato_corregido = {
    "employee_number": "employee_number",
    # Aquí ocurre la magia: mapeamos el origen en español al alias en inglés.
    "costo_diario_operativo": "daily_rate",
}

# Generamos la vista final filtrando las nuevas llaves y renombrándolas.
vista_para_powerbi_final = df_nucleo_bd_nuevo[list(contrato_corregido.keys())].rename(
    columns=contrato_corregido
)

# Imprimimos el resultado para confirmar que el dashboard no sufrirá daños.
print("\nVista final entregada a Power BI (Cambio invisible con éxito):")
print(vista_para_powerbi_final.head(1))
print("\n")
