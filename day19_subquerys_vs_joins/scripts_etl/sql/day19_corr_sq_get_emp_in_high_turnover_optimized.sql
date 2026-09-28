/*******************************************************************************
Título: Consulta Optimizada de Empleados en Puestos de Alto Riesgo de Rotación

Objetivo: Obtener de forma eficiente los datos de empleados en puestos críticos.

Descripción: La consulta realiza un cruce directo (INNER JOIN) entre la tabla de
empleados y el catálogo de puestos, filtrando directamente en la cláusula WHERE
aquellos puestos clasificados con alto riesgo de rotación.

Archivo SQL: day19_corr_sq_get_emp_in_high_turnover_optimized.sql

Archivo CSV: day19_corr_sq_get_emp_in_high_turnover_optimized.csv

Archivo PNG: day19_corr_sq_get_emp_in_high_turnover_optimized.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta Optimizada mediante Cruce Directo (JOIN)
-- Objetivo: Filtrar eficientemente empleados en puestos con alto riesgo
-- ============================================================================

-- Selección de atributos clave
SELECT
    e.employee_number,
    j.department,
    j.job_role,
    e.monthly_income

-- Tabla principal de empleados
FROM fact_employees AS e

-- Cruce con catálogo de puestos
INNER JOIN dim_jobs AS j
    ON e.job_id = j.job_id

-- Filtro por puestos de alto riesgo
WHERE
    j.high_turnover_risk = 'Yes';