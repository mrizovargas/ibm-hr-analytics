--  SOLUCIÓN 2: Agrupar o desduplicar la tabla secundaria antes de la unión (Subconsulta/CTE previa)

/*******************************************************************************
Título: Deduplicación Previa de Dimensión Mediante CTE

Objetivo: Evitar duplicación de filas de empleados mediante catálogo limpio

Descripción: Utiliza una CTE para extraer registros únicos del catálogo 
de puestos antes de realizar el cruce con la tabla principal.

Archivo SQL: day19_deduplicate_dim_before_join_sq.sql

Archivo CSV: day19_deduplicate_dim_before_join_sq.csv

Archivo PNG: day19_deduplicate_dim_before_join_sq.png
*******************************************************************************/

-- ============================================================================
-- BLOQUE 1: Creación de Vista Temporal Desduplicada
-- Objetivo: Aislar valores únicos de puestos para evitar duplicados en cruce
-- ============================================================================

WITH dim_jobs_unicas AS (
    -- Subconsulta: Registros únicos de IDs, puestos y áreas
    SELECT DISTINCT
        job_id,
        job_role,
        department
    FROM dim_jobs
)

-- ============================================================================
-- BLOQUE 2: Consulta Principal y Cruce con Vista Limpia
-- Objetivo: Combinar datos de empleados con el catálogo desduplicado
-- ============================================================================

-- Selección de datos: ID, departamento, rol e ingreso
SELECT
    e.employee_number,
    j.department,
    j.job_role,
    e.monthly_income

-- Tabla de hechos de empleados
FROM fact_employees AS e

-- Cruce con CTE de puestos desduplicados
INNER JOIN dim_jobs_unicas AS j
    ON e.job_id = j.job_id;