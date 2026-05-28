# ==============================================================================
# Título: Radar de Talento y Segmentación de Riesgo de RRHH
#
# Objetivo:Identificar de forma automatizada a los empleados en situación crítica
# dentro de la empresa para apoyar las estrategias de retención de talento.
#
# Descripción: El script lee un archivo de datos históricos de Recursos Humanos,
# limpia y normaliza los nombres de las columnas a un formato estandarizado,
# limpia los espacios en blanco en los textos y filtra de forma masiva (vectorizada)
# a los empleados que cumplen con dos condiciones de riesgo: baja satisfacción
# laboral y un sueldo inferior al promedio global de la compañía.
#
# Archivo Python: day08_vectorized_filter.py
#
# Archivo CSV: day08_empl_attrition_risk.csv
#
# Archivo PNG: day08_vectorized_filter.png
# ==============================================================================

# ==========================================
# --- BLOQUE 1: IMPORTACIÓN DE LIBRERÍAS ---
# ==========================================
# Herramienta fundamental para manipular y analizar datos en formato de tabla.
import pandas as pd

# Biblioteca nativa para interactuar con el sistema operativo y carpetas de tu computadora.
import os

# Módulo moderno para interactuar con el sistema de archivos y manejar rutas de carpetas/archivos de forma multiplataforma.
from pathlib import Path

# Permite mostrar y registrar mensajes informativos en la consola sobre el avance del script.
import logging

# Biblioteca para buscar, extraer o reemplazar patrones complejos de texto.
import re

# Módulo para trabajar con fechas y horas (por ejemplo, obtener la fecha actual o dar formato al tiempo)
from datetime import datetime

# ===========================================
# --- BLOQUE 2: CONFIGURACIÓN DEL ENTORNO ---
# ===========================================
# Configura el formato de los mensajes en consola, añadiendo la hora exacta, el tipo de mensaje y su contenido.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Define la función principal que ejecutará todo el análisis y devolverá un indicador de éxito (Verdadero/Falso).
def ejecutar_radar_talento() -> bool:

    # ==================================================
    # --- BLOQUE 3: RUTAS Y VERIFICACIÓN DE ARCHIVOS ---
    # ==================================================
    # Busca la ubicación del archivo actual y sube 3 carpetas para llegar a la raíz del proyecto.
    base_dir = Path(__file__).resolve().parents[3]

    # Construye la ruta hacia la carpeta específica donde se guardan los datos crudos de RRHH.
    target_raw_dir = base_dir / "02_data" / "raw" / "rrhh"

    # Ruta destino para guardar los registros de los empleados en riesgo
    target_processed_dir = base_dir / "02_data" / "processed" / "rrhh"

    # Define el nombre del archivo de datos sin la extensión.
    rrhh_file_name = "WA_Fn-UseC_-HR-Employee-Attrition"

    # Une la ruta de la carpeta y el nombre del archivo con la extensión .csv.
    rrhh_path_csv = os.path.join(target_raw_dir, f"{rrhh_file_name}.csv")

    # Revisa si el archivo CSV realmente existe en la ruta calculada antes de continuar.
    if not os.path.exists(rrhh_path_csv):
        # Registra en la consola que el archivo no fue encontrado.
        print("\n")
        logging.info("====== INGESTA ======")
        logging.info(f"❌ Archivo origen no localizado en la ruta: {rrhh_path_csv}")
        print("\n")
        # Detiene la ejecución del script indicando que falló.
        return False

    # Inicia un bloque de seguridad para capturar cualquier fallo inesperado durante el procesamiento.
    try:

        # ========================================================
        # --- BLOQUE 4 (LÓGICO): REGLAS DE CONVERSIÓN DE TEXTO ---
        # ========================================================

        # Función interna para convertir nombres tipo 'ColumnaEjemplo' a 'columna_ejemplo'.
        def to_snake_case(name):
            """Convierte un texto de formato CamelCase o PascalCase a snake_case."""
            # Inserta un guion bajo entre una letra minúscula y una mayúscula (ej: "EmpleadoId" -> "Empleado_Id").
            s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)

            # Controla números o mayúsculas juntas y pasa todo el texto a letras minúsculas de forma limpia.
            return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

        # ============================================================
        # --- BLOQUE 5 (LÓGICO): CARGA Y NORMALIZACIÓN DE COLUMNAS ---
        # ============================================================

        # Inicia un sub-bloque de seguridad exclusivo para la lectura y limpieza inicial de la tabla.
        try:
            # Avisa en la consola que se está iniciando la lectura de los datos.
            print("\n")
            logging.info("====== INGESTA ======")
            logging.info("⏳ Leyendo archivo original...")

            # Lee el archivo de texto CSV y lo transforma en una tabla digital manipulable (DataFrame).
            df = pd.read_csv(rrhh_path_csv)

            # Avisa en la consola que se está iniciando el proceso de limpieza estética.
            logging.info("🛠️ Limpiando y transformando datos...")

            # Transforma los títulos de todas las columnas usando la función de conversión a minúsculas con guiones bajos.
            df.columns = [to_snake_case(col) for col in df.columns]

            # Corrige manualmente el caso especial de la columna 'over18' para que coincida con el estándar de base de datos.
            df.rename(columns={"over18": "over_18"}, inplace=True)

            # Recorre cada celda de la tabla y, si detecta un texto, le borra los espacios vacíos innecesarios en los extremos.
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Si ocurre un error al leer o limpiar la tabla, se activa esta sección.
        except Exception as error_proceso:
            # Registra el error específico en la consola para saber exactamente qué falló.
            logging.info(f"❌ Error al cargar o procesar el dataset: {error_proceso}")
            print("\n")
            # Detiene la ejecución del script indicando que falló en la fase de carga.
            return False

        # ==============================================================
        # --- BLOQUE 6 (LÓGICO): FILTRADO MULTI-CRITERIO VECTORIZADO ---
        # ==============================================================

        # Calcula la media salarial global de toda la empresa para usarla como métrica de referencia.
        salario_medio_global = df["monthly_income"].mean()

        # Muestra en consola el salario promedio global calculado con un formato de dos decimales.
        logging.info(
            f"📊 El salario promedio global de la empresa es: ${salario_medio_global:.2f} USD."
        )

        # Avisa en consola que se va a iniciar la búsqueda inteligente de empleados en riesgo.
        logging.info("🛰️ Aplicando Filtrado Multi-Criterio Vectorizado...")

        # Crea una regla de búsqueda: Empleados con baja satisfacción (valores 1 o 2 en la escala interna).
        condicion_baja_satisfaccion = df["job_satisfaction"] <= 2

        # Crea una segunda regla de búsqueda: Empleados con un sueldo mensual por debajo del promedio global.
        condicion_salario_bajo = df["monthly_income"] < salario_medio_global

        # Une ambas reglas en una sola consulta para extraer únicamente a los empleados que cumplen las dos condiciones.
        df_empleados_en_riesgo = df[
            condicion_baja_satisfaccion & condicion_salario_bajo
        ]

        # Informa en consola que el proceso de segmentación y filtrado terminó correctamente.
        logging.info("✅ ====== SEGMENTACIÓN COMPLETADA ======")
        logging.info("✅ ¡La segmentación ha sido completada con éxito!")

        # Muestra en la pantalla la cantidad total de empleados que tiene la empresa originalmente.
        print(f"\nTotal de empleados en la compañía: {len(df)}")

        # Muestra en la pantalla cuántos empleados específicos cumplen con el perfil de riesgo detectado.
        print(
            f"Cantidad de empleados en riesgo (Poca satisfacción + Bajo sueldo): {len(df_empleados_en_riesgo)}"
        )

        # Imprime un encabezado estético para la vista previa de los datos filtrados.
        print("\n👀 Vista previa de la población crítica detectada:")

        # Filtramos nuestra base de datos (df) para quedarnos solo con la información de los empleados que están en riesgo.
        col_empleados_en_riesgo = df_empleados_en_riesgo[
            [
                "employee_id",  # Identificador único del empleado
                "employee_number",  # Número de registro del empleado
                "department",  # Área o departamento donde trabaja
                "job_role",  # Puesto o rol que ocupa
                "job_satisfaction",  # Nivel de satisfacción laboral
                "monthly_income",  # Ingreso o salario mensual
            ]
        ].head()  # Limitamos el resultado para mostrar únicamente las primeras filas

        # Muestra en pantalla una tabla pequeña con los primeros 5 empleados en riesgo, detallando sus datos clave.
        # to_string(index=False) asegura que los números de fila automáticos no se muestren, dejando la tabla mucho más limpia.
        print(col_empleados_en_riesgo.to_string(index=False))

        # ===================================================================
        # --- BLOQUE 7 (LÓGICO): EXPORTAMOS RESULTADOS A UN ARCHIVO "CSV" ---
        # ===================================================================
        # Procedemos a exportar las filas con fallas de integridad a la carpeta destino
        try:
            # Crea de forma segura la estructura de directorios si aún no existe en el disco duro
            target_processed_dir.mkdir(parents=True, exist_ok=True)

            # Obtenemos la fecha y hora exactas para crear un identificador
            # Formato: AñoMesDía_HoraMinutoSegundo (ej. 20260523_153900)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Genera una ruta de destino para el archivo que contiene errores o rechazos.
            emp_attrition_risk_file_name = f"day08_empl_attrition_risk_{timestamp}.csv"
            emp_attrition_risk_file_path = (
                target_processed_dir / emp_attrition_risk_file_name
            )

            # Exportamos a formato CSV sin el índice por defecto de pandas
            df_empleados_en_riesgo.to_csv(
                emp_attrition_risk_file_path, index=False, encoding="utf-8"
            )
            print("\n")
            logging.info("✅ ====== TRANSFERENCIA COMPLETA ======")
            logging.info(
                f"💾 Respaldo de resultados exportado con éxito en: {target_processed_dir}"
            )
            logging.info(f"📄 CSV: {emp_attrition_risk_file_name}")

        except Exception as e_export:
            logging.info(
                f"❌ Alerta: No se pudo exportar el archivo de auditoría local: {e_export}"
            )
            print("\n")

        print("\n")
        # Finaliza con éxito la función principal devolviendo un indicador verdadero.
        return True

    # Si ocurre un error grave e inesperado en cualquier otra parte del flujo, se activa esta sección.
    except Exception as error_proceso:
        # Registra el mensaje de error crítico en la consola para facilitar el diagnóstico técnico.
        logging.info(f"❌ Error crítico detectado durante el proceso: {error_proceso}")
        print("\n")
        # Detiene la ejecución del script indicando que ocurrió un colapso general.
        return False


# ===========================================
# --- BLOQUE 8 (LÓGICO): PUNTO DE ENTRADA ---
# ===========================================
# Valida si este archivo se está ejecutando de forma directa en la computadora en lugar de ser importado por otro script.
if __name__ == "__main__":
    # Da la orden de arrancar todo el proceso del radar de talento que definimos arriba.
    ejecutar_radar_talento()
