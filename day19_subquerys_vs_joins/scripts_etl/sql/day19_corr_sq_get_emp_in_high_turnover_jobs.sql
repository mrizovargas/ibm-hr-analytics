/*******************************************************************************
Título: Empleados y Puestos con Alto Riesgo de Rotación mediante JOIN y EXISTS

Objetivo: Obtener la información de los empleados cuyo puesto actual presenta
un alto riesgo de rotación.

Descripción: La consulta une la tabla principal de empleados con el catálogo de
puestos para extraer el departamento y utiliza una subconsulta correlacionada
con EXISTS para validar y filtrar únicamente los puestos marcados con alto
riesgo de rotación.

Archivo SQL: day19_corr_sq_get_emp_in_high_turnover_jobs.sql

Archivo PNG: day19_corr_sq_get_emp_in_high_turnover_jobs.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta de Empleados en Puestos Críticos por Rotación
-- Objetivo: Filtrar los empleados que pertenecen a puestos con alto riesgo
-- ============================================================================

-- Selección de atributos clave
SELECT
    e.employee_number,
    j1.department,
    e.job_id,
    e.monthly_income

-- Tabla principal de empleados
FROM
    fact_employees AS e

-- Cruce con catálogo de puestos
INNER JOIN dim_jobs AS j1
    ON e.job_id = j1.job_id

-- Validación de existencia en puestos de alto riesgo
WHERE EXISTS (

    -- Subconsulta correlacionada por puesto y nivel de riesgo
    SELECT 1
    FROM
        dim_jobs AS j2
    WHERE
        j2.job_id = e.job_id
        AND j2.high_turnover_risk = 'Yes'
);