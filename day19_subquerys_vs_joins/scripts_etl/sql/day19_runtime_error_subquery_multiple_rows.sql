/*******************************************************************************
Título: Demostración de Error de Runtime por Subconsulta Multifila

Objetivo: Ilustrar el fallo de ejecución al comparar escalar contra varias filas

Descripción: Al incluir GROUP BY interno, la subconsulta retorna múltiples 
filas, causando un error en tiempo de ejecución con el operador '>'.

Archivo SQL: day19_runtime_error_subquery_multiple_rows.sql

Archivo PNG: day19_runtime_error_subquery_multiple_rows.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta con Error de Subconsulta Multifila
-- Objetivo: Intentar un filtro con comparador escalar frente a múltiples valores
-- ============================================================================

-- Selección de datos clave a mostrar: ID, departamento, rol e ingreso
SELECT
    f.employee_number,
    d.department,
    d.job_role,
    f.monthly_income

-- Tabla principal de hechos de empleados
FROM
    fact_employees AS f

-- Cruce con el catálogo de puestos por ID de empleo
JOIN dim_jobs AS d
    ON f.job_id = d.job_id

-- Filtro con error de comparación escalar frente a múltiples filas
WHERE
    f.monthly_income > (

        -- Subconsulta: Promedio por puesto que genera múltiples resultados
        SELECT
            AVG(monthly_income)
        FROM
            fact_employees

        -- Agrupación que origina el fallo de tiempo de ejecución
        GROUP BY job_id
    );