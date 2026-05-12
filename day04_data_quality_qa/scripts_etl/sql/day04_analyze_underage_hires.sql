/*******************************************************************************
Título: Análisis de Contrataciones Menores de Edad

Objetivo: Identificar empleados contratados antes de cumplir los 18 años.

Descripción: Esta consulta selecciona datos básicos de empleados y calcula su 
edad de contratación para detectar posibles inconsistencias o incumplimientos 
de políticas de edad laboral.

Archivo SQL: day04_analyze_underage_hires.sql

Archivo CSV: day04_analyze_underage_hires.csv

Archivo PNG: day04_analyze_underage_hires.png
*********************************************************************************/

SELECT 
    employee_number,          -- Identificador único del empleado
    age,                      -- Edad actual del empleado
    years_at_company,         -- Años de antigüedad en la empresa
    -- Cálculo: Resta la antigüedad a la edad actual para estimar la edad al contratar
    (age - years_at_company) AS hire_age 
FROM 
    employee_master_data      -- Tabla que contiene la información maestra de empleados
WHERE 
    -- Filtro: Muestra solo casos donde la edad de contratación calculada es menor a 18
    (age - years_at_company) < 18;