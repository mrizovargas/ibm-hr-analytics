/*******************************************************************************
Título: Análisis de Calidad de Datos en Registro de Empleados

Objetivo: Identificar inconsistencias lógicas en los datos maestros de empleados.

Descripción: Este script busca empleados con datos ilógicos en sus fechas de 
             promoción (promociones antes de entrar) o edades de contratación 
             imposibles (menores de edad), permitiendo limpiar la base de datos.

Archivo SQL: day04_analyze_empl_data_quality.sql

Archivo CSV: day04_analyze_empl_data_quality_01.csv
			 day04_analyze_empl_data_quality_02.csv

Archivo PNG: day04_analyze_empl_data_quality_01.png
			 day04_analyze_empl_data_quality_02.png
**********************************************************************************/

-- BLOQUE 1: Detectar anomalías en años de promoción
-- Selecciona empleados cuyo tiempo desde la última promoción es mayor a su antigüedad total,
-- lo cual indica un error de captura de datos.
SELECT 
    employee_number,            -- Identificador único del empleado
    years_at_company,           -- Antigüedad total en la empresa
    years_since_last_promotion  -- Años desde la última promoción
FROM
    employee_master_dirty_data
WHERE 
    -- Filtro: La promoción no puede ocurrir antes del ingreso
    years_since_last_promotion > years_at_company;


-- BLOQUE 2: Identificar contratación de menores de edad
-- Calcula la edad de contratación y selecciona a quienes ingresaron con menos de 18 años,
-- para revisión de cumplimiento normativo.
SELECT 
    employee_number,
    age,                        -- Edad actual del empleado
    years_at_company,
    (age - years_at_company) AS hire_age  -- Cálculo: Edad actual - Años en empresa
FROM 
    employee_master_dirty_data
WHERE 
    -- Filtro: Edad de contratación menor a 18 años
    (age - years_at_company) < 18;