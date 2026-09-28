-- CÓDIGO INEFICIENTE

/*******************************************************************************
Título: Consulta de Empleados del Departamento de Ventas mediante IN

Objetivo: Identificar empleados del área de Ventas usando una lista

Descripción: Genera los identificadores de puesto de Ventas en la tabla de 
dimensiones y filtra la tabla principal de empleados.

Archivo SQL: day19_sq_in_get_sales_employees.sql

Archivo CSV: day19_sq_in_get_sales_employees.csv

Archivo PNG: day19_sq_in_get_sales_employees.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta de Empleados por Departamento con Subconsulta IN
-- Objetivo: Filtrar empleados basándose en la lista de puestos de Ventas
-- ============================================================================

-- Selección de datos básicos del empleado
SELECT
    employee_number,
    job_id,
    monthly_income

-- Tabla principal de empleados
FROM fact_employees

-- Filtro por puesto contenido en la lista de Ventas
WHERE job_id IN (

    -- Subconsulta: Identificadores de puesto del área de Ventas
    SELECT job_id
    FROM dim_jobs
    WHERE department = 'Sales'
);