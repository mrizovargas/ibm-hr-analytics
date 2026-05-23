/*******************************************************************************
Título: Documentación del Diccionario de Datos - Tabla Maestra de Empleados

Objetivo: Registrar las descripciones oficiales de la tabla y sus columnas en la 
base de datos.

Descripción: Este script utiliza comandos 'COMMENT ON' dentro de una transacción 
segura para guardar metadatos sobre la estructura de empleados (IBM Dataset). 
Esto permite que cualquier usuario o herramienta entienda el significado exacto de 
cada campo sin depender de manuales externos.

Archivo SQL: day06_empl_mstr_data_tbl_and_col_comments.sql

Archivo PNG: day06_empl_mstr_data_tbl_and_col_comments.png
********************************************************************************/

/***********************************************************
BLOQUE 1: TRANSACCIÓN
***********************************************************/
-- Asegura que todos los comentarios se guarden juntos. 
-- Si algo falla, no se aplica ningún cambio parcial.
BEGIN;

-- 1. DOCUMENTACIÓN DE LA TABLA PRINCIPAL
-- Se registra el propósito general de la tabla en el motor de la base de datos.
COMMENT ON TABLE employee_master_data 
IS 'Tabla maestra de empleados para el Sprint de 120 días - IBM Dataset';

-- 2. DOCUMENTACIÓN DE COLUMNAS DE IDENTIFICACIÓN Y PERFIL
-- Explicación de los campos que identifican y describen la preparación del empleado.
COMMENT ON COLUMN employee_master_data.employee_id
IS 'Identificador único (ID) del empleado';

COMMENT ON COLUMN employee_master_data.education 
IS 'Nivel educativo alcanzado';

-- 3. DOCUMENTACIÓN DE MÉTRICAS DE SATISFACCIÓN Y COMPROMISO
-- Bloque de campos numéricos que miden el clima laboral y la percepción del personal.
COMMENT ON COLUMN employee_master_data.environment_satisfaction 
IS 'Nivel de satisfacción con el entorno laboral';

COMMENT ON COLUMN employee_master_data.job_involvement 
IS 'Grado de compromiso con el trabajo';

COMMENT ON COLUMN employee_master_data.job_satisfaction 
IS 'Nivel de satisfacción con el puesto actual';

COMMENT ON COLUMN employee_master_data.relationship_satisfaction 
IS 'Nivel de satisfacción en las relaciones laborales';

COMMENT ON COLUMN employee_master_data.work_life_balance 
IS 'Equilibrio entre la vida personal y laboral';

-- 4. DOCUMENTACIÓN DE COMPENSACIONES Y SALARIOS
-- Bloque financiero que detalla los ingresos económicos en sus distintas modalidades y reglas.
COMMENT ON COLUMN employee_master_data.monthly_income 
IS 'Ingreso mensual bruto del empleado en USD (Validado > 0)';

COMMENT ON COLUMN employee_master_data.daily_rate
IS 'Tarifa diaria de pago';

COMMENT ON COLUMN employee_master_data.hourly_rate
IS 'Tarifa por hora de pago';

COMMENT ON COLUMN employee_master_data.monthly_rate
IS 'Tasa o tarifa mensual asignada';

COMMENT ON COLUMN employee_master_data.percent_salary_hike
IS 'Porcentaje de incremento salarial último';

-- 5. DOCUMENTACIÓN DE TIEMPO Y CONTROL OPERATIVO
-- Campos utilizados para la contabilidad de horas y estadísticas internas.
COMMENT ON COLUMN employee_master_data.standard_hours
IS 'Número estándar de horas laborales';

COMMENT ON COLUMN employee_master_data.employee_count
IS 'Conteo de empleados (usualmente valor constante 1)';

-- Cierre de Transacción: Confirma y aplica de forma permanente todos los comentarios anteriores.
COMMIT;


/***********************************************************
BLOQUE 2: SELECCIÓN DE DATOS (Bloque lógico principal)
***********************************************************/
-- 5. Se extraen los campos necesarios para el reporte de RRHH.
SELECT 
    employee_id,    -- Identificador único del empleado
    age,            -- Edad del empleado para análisis demográfico
    monthly_income  -- Ingreso bruto mensual para análisis salarial
FROM 
    employee_master_data; -- Tabla origen definida en el paso 1