-- CÓDIGO OPTIMIZADO (Reescritura relacional con INNER JOIN)

/*******************************************************************************
Título: Consulta Optimizada de Empleados del Departamento de Ventas

Objetivo: Obtener datos de empleados del área de Ventas de forma eficiente

Descripción: Cruce directo (INNER JOIN) entre tabla de hechos y catálogo de puestos 
filtrando el departamento en WHERE.

Archivo SQL: day19_sq_inner_join_get_sales_emp_optimized.sql

Archivo CSV: day19_sq_inner_join_get_sales_emp_optimized.csv

Archivo PNG: day19_sq_inner_join_get_sales_emp_optimized.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta Optimizada de Empleados por Departamento
-- Objetivo: Unir tablas y filtrar empleados pertenecientes a Ventas
-- ============================================================================

-- Selección de datos: ID, departamento, rol e ingreso
SELECT
    e.employee_number,
    j.department,
    j.job_role,
    e.monthly_income

-- Tabla de hechos de empleados
FROM fact_employees AS e

-- Cruce con dimensión de puestos por ID de puesto
INNER JOIN dim_jobs AS j
    ON e.job_id = j.job_id

-- Filtro por departamento de Ventas
WHERE j.department = 'Sales';