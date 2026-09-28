-- ERROR: Genera duplicados en los registros de empleados

/*******************************************************************************
Título: Riesgo de Duplicación de Empleados por Claves Duplicadas en Dimensión

Objetivo: Ejemplificar la duplicación de filas por datos repetidos en catálogo

Descripción: Al cruzar empleados con puestos, si el catálogo contiene IDs duplicados, 
se multiplicarán los registros de empleados resultantes.

Archivo SQL: day19_duplicate_records_risk_from_non_unique_dim.sql
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta de Empleados con Riesgo de Duplicidad por JOIN
-- Objetivo: Cruzar empleados con puestos asumiendo un potencial problema de llaves
-- ============================================================================

-- Selección del número de nómina y salario mensual
SELECT
    e.employee_number,
    e.monthly_income

-- Tabla de hechos de empleados
FROM fact_employees AS e

-- Cruce con dimensión de puestos por ID (duplica filas si job_id se repite)
INNER JOIN dim_jobs AS j
    ON e.job_id = j.job_id;