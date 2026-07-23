"""
=======================================================================
Título: Pipeline de Alertas Salariales (Script con Error de Ejecución)

Objetivo: Demostrar cómo un desajuste entre el número de condiciones y
etiquetas provoca que el programa falle por completo.

Descripción: Este script intenta clasificar los sueldos en tres niveles
de puesto. El error fatal ocurre porque definimos tres reglas o escenarios
(condiciones), pero solo le dimos al programa dos respuestas posibles
(opciones). Al no haber un emparejamiento exacto, Python frena la
ejecución.

Archivo Python: day14_failed_salary_analysis_test.py
=======================================================================
"""

# =====================================================================
# BLOQUE 1: REQUISITOS PREVIOS DEL SISTEMA
# Objetivo: Cargar las librerías necesarias para el procesamiento.
# =====================================================================
# Traemos NumPy para aplicar las reglas en bloque
import numpy as np

# Traemos Pandas para la manipulación de la tabla de datos
import pandas as pd

# =====================================================================
# BLOQUE 2: DEFINICIÓN DE REGLAS Y EL ERROR DE DESAJUSTE
# Objetivo: Configurar las condiciones de negocio y las etiquetas.
# =====================================================================
# NOTA: Para que este bloque funcione, la tabla 'df' ya debería estar
# cargada en memoria. Aquí asumimos que existe para evaluar la lógica.

# ERROR: Aquí creamos una lista que contiene exactamente 3 condiciones
condiciones_erroneas = [
    # Condición 1: Empleados de nivel 1 con sueldo menor a 2800
    (df["JobLevel"] == 1) & (df["MonthlyIncome"] < 2800),
    # Condición 2: Empleados de nivel 2 con sueldo menor a 5500
    (df["JobLevel"] == 2) & (df["MonthlyIncome"] < 5500),
    # Condición 3: Empleados de nivel 3 con sueldo menor a 9000
    (df["JobLevel"] == 3) & (df["MonthlyIncome"] < 9000),
]

# ERROR: Aquí está el detonante del fallo. Solo pusimos 2 opciones.
opciones_erroneas = [
    "N1_Por_Debajo_Mercado",  # Respuesta para la Condición 1
    "N2_Por_Debajo_Mercado",  # Respuesta para la Condición 2
    # ¡ALERTA! Falta escribir la respuesta para la Condición 3
]


# =====================================================================
# BLOQUE 3: EJECUCIÓN DE LA FUNCIÓN Y RUPTURA DEL PIPELINE
# Objetivo: Intentar procesar los datos combinando las listas previas.
# =====================================================================
# Al correr esta línea, la librería NumPy se dará cuenta de que tiene
# 3 preguntas pero solo 2 respuestas. Al no saber qué etiqueta ponerle
# a la condición número 3, arrojará un error de tipo 'ValueError'.
df["Estatus_Compensacion"] = np.select(
    condiciones_erroneas,
    opciones_erroneas,
    default="Competitivo",  # Si no cumple ninguna, el sueldo es bueno
)
