-- SOLUCIÓN 1: Aplicar DISTINCT si solo necesitas columnas de la tabla de hechos

/*******************************************************************************
Título: Eliminación de Filas Duplicadas mediante la Cláusula DISTINCT

Objetivo: Garantizar registros únicos de empleados al consultar columnas de 
hechos

Descripción: Une la tabla de hechos con la dimensión de puestos y usa DISTINCT 
para remover filas repetidas causadas por claves duplicadas en el catálogo.

Archivo SQL: day19_deduplicate_emp_records_with_distinct.sql

Archivo PNG: day19_deduplicate_emp_records_with_distinct.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Consulta de Empleados Únicos con Filtro de Duplicados
-- Objetivo: Obtener la lista limpia de empleados evitando filas repetidas por 
-- JOIN
-- ============================================================================

-- Selección de registros únicos: número de nómina e ingreso mensual
SELECT DISTINCT
    e.employee_number,
    e.monthly_income

-- Tabla de hechos de empleados
FROM fact_employees AS e

-- Cruce con dimensión de puestos para validar la relación de tablas
INNER JOIN dim_jobs AS j
    ON e.job_id = j.job_id;