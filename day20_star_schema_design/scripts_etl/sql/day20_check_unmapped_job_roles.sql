/*******************************************************************************
 Título: Validación de Integridad de Puestos (Roles Huérfanos sin Clave Surrogada)

 Objetivo: Identificar roles de trabajo presentes en la tabla maestra de empleados 
 que no tengan una coincidencia o clave asignada en el catálogo de puestos.

 Descripción: Realiza un cruce (LEFT JOIN) entre los datos maestros y la dimensión 
 de puestos para detectar roles no catalogados (j.sk_job_id IS NULL) y asegurar 
 la integridad referencial del modelo.

 Archivo SQL: day20_check_unmapped_job_roles.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CONSULTA DE CONTROL Y VALIDACIÓN DE INTEGRIDAD REFERENCIAL
-- Objetivo: Detectar puestos de empleados que no existen en el catálogo.
-- Nota: Si esta consulta devuelve filas, esos roles no existen en dim_jobs_new y debes 
-- agregarlos antes de ejecutar la inserción.
-- ====================================================================================

SELECT DISTINCT 
    e.job_role               -- Lista los títulos de puestos únicos sin duplicados
FROM 
    employee_master_data AS e -- Tabla maestra origen que contiene los empleados
LEFT JOIN 
    dim_jobs_new AS j ON e.job_role = j.job_role -- Une con el catálogo según el rol
WHERE 
    j.sk_job_id IS NULL;     -- Filtra únicamente los puestos que no hicieron cruce