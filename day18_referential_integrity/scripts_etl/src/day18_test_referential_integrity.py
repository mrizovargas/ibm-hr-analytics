# =====================================================================
# Título: Prueba de Integridad Referencial en Base de Datos
#
# Objetivo: Verificar que la base de datos bloquee la inserción de datos
# no válidos.
#
# Descripción: El script intenta insertar un empleado ficticio asociado
# a un puesto de trabajo inexistente para confirmar que las reglas de
# seguridad y llaves foráneas de PostgreSQL funcionen correctamente.
#
# Archivo Python: day18_test_referential_integrity.py
#
# Archivo PNG: day18_test_referential_integrity_flow.png
# =====================================================================

# =====================================================================
# BLOQUE 1: Importación de Librerías y Ajuste de Rutas
# Objetivo: Cargar los módulos necesarios y configurar el acceso a
#           funciones personalizadas del proyecto.
# =====================================================================

# Herramienta principal para manipular y estructurar datos en tablas
import pandas as pd

# Módulo del sistema para controlar la salida y rutas del programa
import sys

# Módulo para registrar eventos e historial durante la ejecución
import logging

# Herramienta para manejar rutas de archivos de forma independiente
from pathlib import Path

# Excepción de SQLAlchemy cuando se violan reglas de la base de datos
from sqlalchemy.exc import IntegrityError

# Excepción nativa de PostgreSQL cuando falla una llave foránea
from psycopg2.errors import ForeignKeyViolation

# Excepción de Pandas que envuelve errores de la base de datos
from pandas.errors import DatabaseError

# Calculamos la ruta del directorio raíz para importar nuestros módulos
src_dir = str(Path(__file__).resolve().parents[1])

# Añadimos la ruta del proyecto al sistema si no está registrada
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Cargamos nuestras funciones internas para el registro y conexión
from custom_functions.logging_pipeline import get_logging_pipeline
from custom_functions.security_engine import get_secure_engine

# Activamos el sistema de registro de eventos (logs) del proceso
get_logging_pipeline()


# =====================================================================
# BLOQUE 2: Definición de la Prueba de Integridad
# Objetivo: Intentar insertar un registro inválido para validar los
#           candados de seguridad de la base de datos.
# =====================================================================


def test_referencial_integrity_violation() -> bool:
    """Intenta insertar un registro huérfano para probar la BD."""
    print("\n")
    logging.info("🚀 ==== INICIANDO CONEXIÓN CON POSTGRESQL ====")

    try:
        # Abrimos la conexión segura con las credenciales de la base
        engine = get_secure_engine()

        # Preparamos una consulta sencilla para revisar empleados
        query = """
            SELECT *
            FROM fact_employees;
        """

        # Leemos los datos existentes dentro de una tabla de Pandas
        df = pd.read_sql(query, con=engine)

        # Si encontramos datos, procedemos con la prueba de seguridad
        if not df.empty:
            logging.info(
                "🚀 ==== INICIANDO VALIDACIÓN DE EXCEPCIONES "
                "(INTEGRIDAD REFERENCIAL) ===="
            )

            # Creamos un empleado de prueba con un puesto inexistente
            invalid_employee = pd.DataFrame(
                [
                    {
                        "employee_number": 99999,
                        "job_id": 9999,  # Puesto 9999 no existe
                        "age": 47,
                        "attrition": "No",
                        "monthly_income": 5000,
                    }
                ]
            )

            print(
                "\n⚡ Intentando insertar un registro huérfano para "
                "prueba de estrés..."
            )

            # Intentamos guardar el empleado no válido en la base
            invalid_employee.to_sql(
                "fact_employees",
                con=engine,
                if_exists="append",
                index=False,
            )

            # Si la base lo permite, significa que la regla falló
            print("⚠️ ALERTA: La BD permitió insertar datos corruptos")
            return False

        else:
            # Notificamos si la tabla de empleados está completamente vacía
            logging.info("❌ No se encontraron registros en la tabla principal.")
            print("\n")
            return False

    except (DatabaseError, IntegrityError, ForeignKeyViolation) as e:
        # Si entra aquí, la base de datos bloqueó con éxito la inserción
        logging.info(
            "✅ PRUEBA EXITOSA: La Integridad Referencial bloqueó el "
            "registro huérfano."
        )
        print(f"\n🔒 Detalle del bloqueo en PostgreSQL: {e}")
        print("\n")
        return True


# =====================================================================
# BLOQUE 3: Punto de Entrada Principal
# Objetivo: Ejecutar la prueba y evaluar el resultado final del script.
# =====================================================================

if __name__ == "__main__":
    # Corremos la prueba de validación y guardamos su resultado
    success = test_referencial_integrity_violation()

    # Si la prueba no fue exitosa o no se pudo hacer, detenemos todo
    if not success:
        sys.exit(1)
