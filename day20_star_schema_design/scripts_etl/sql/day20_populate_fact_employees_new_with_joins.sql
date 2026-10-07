/*******************************************************************************
 Título: Vaciado y Carga Total de la Tabla de Hechos de Empleados (fact_employees)

 Objetivo: Reiniciar la tabla central de hechos y volver a poblarla asociando cada 
 empleado con sus llaves técnicas de puestos y demografía.

 Descripción: Limpia la tabla fact_employees reseteando contadores e inserta métricas 
 operativas actualizadas conectando employee_master_data con dim_jobs y 
 dim_demographics.

 Archivo SQL: day20_populate_fact_employees_new_with_joins.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: REINICIO Y VACIADO DE LA TABLA DESTINO
-- Objetivo: Vaciar la tabla de hechos y reiniciar contadores e identificadores.
-- ====================================================================================

TRUNCATE TABLE fact_employees_new RESTART IDENTITY CASCADE;      -- Vacía la tabla de hechos y reinicia los IDs

-- ====================================================================================
-- BLOQUE 2: DEFINICIÓN DE ESTRUCTURA Y COLUMNAS DE DESTINO
-- Objetivo: Especificar la tabla y campos receptores dentro de la tabla de hechos.
-- ====================================================================================

INSERT INTO fact_employees_new (
    employee_number,         -- Número único de nómina del empleado
    sk_job_id,               -- Clave sustituta obtenida de la dimensión de puestos
    sk_demographics_id,      -- Clave sustituta obtenida de la dimensión demográfica
    attrition_numeric,       -- Indicador numérico de rotación (0 = No, 1 = Sí)
    attrition,               -- Estado de rotación expresado en texto (Yes / No)
    monthly_income,          -- Sueldo o ingreso mensual registrado
    years_at_company,        -- Antigüedad en años dentro de la organización
    total_working_years      -- Años totales de experiencia laboral
)

-- ====================================================================================
-- BLOQUE 3: SELECCIÓN Y CRUCE DE DATOS CON DIMENSIONES
-- Objetivo: Consultar métricas y cruzar las dimensiones para vincular sus llaves.
-- ====================================================================================

SELECT 
    e.employee_number,       -- Identificador del empleado desde la tabla maestra
    j.sk_job_id,             -- Llave técnica asignada desde la dimensión puestos
    d.sk_demographics_id,    -- Llave técnica asignada desde la dimensión demografía
    e.attrition_numeric,     -- Indicador numérico de salida laboral
    e.attrition,             -- Condición textual de salida laboral
    e.monthly_income,        -- Salario mensual del colaborador
    e.years_at_company,      -- Años acumulados trabajando en la empresa
    e.total_working_years    -- Años de experiencia profesional total
FROM 
    employee_master_data AS e -- Fuente maestra con los datos generales de empleados
LEFT JOIN 
    dim_jobs_new AS j            -- Une con el catálogo de puestos por título de rol
    ON e.job_role = j.job_role -- Coincidencia exacta por el puesto de trabajo
LEFT JOIN 
    dim_demographics AS d    -- Une con el catálogo demográfico por perfil
    ON e.gender = d.gender   -- Coincidencia por género
    AND e.education_field = d.education_field -- Coincidencia por área académica
    AND e.marital_status = d.marital_status;   -- Coincidencia por estado civil