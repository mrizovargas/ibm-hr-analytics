/*******************************************************************************
Título: Empleados con Salario Superior al Promedio General

Objetivo: Identificar empleados con ingreso superior a la media

Descripción: Calcula el salario promedio global, cruza empleados con 
puestos para obtener departamento y rol, y ordena de mayor a menor ingreso.

Archivo SQL: day19_scalar_subquery.sql

Archivo CSV: day19_scalar_subquery.csv

Archivo PNG: day19_scalar_subquery.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta de Empleados Destacados por Ingreso
-- Objetivo: Cruzar tablas, filtrar salarios sobre el promedio y ordenar
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

-- Filtro para conservar empleados con sueldo superior al promedio general
WHERE
    f.monthly_income > (

        -- Subconsulta: Salario medio mensual de la plantilla
        SELECT
            AVG(monthly_income)
        FROM
            fact_employees
    )

-- Ordenamiento descendente por ingreso mensual
ORDER BY
    f.monthly_income DESC;