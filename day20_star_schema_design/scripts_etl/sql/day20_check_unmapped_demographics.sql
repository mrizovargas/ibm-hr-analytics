/*******************************************************************************
 Título: Validación de Integridad Demográfica (Empleados Huérfanos sin Clave)

 Objetivo: Identificar colaboradores registrados en la tabla maestra que no tengan 
 una coincidencia o clave asignada en la dimensión demográfica.

 Descripción: Realiza un cruce (LEFT JOIN) entre la fuente maestra de empleados y 
 la dimensión demográfica para detectar registros no catalogados 
 (d.sk_demographics_id IS NULL) y garantizar la calidad de los datos.

 Archivo SQL: day20_check_unmapped_demographics.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CONSULTA DE CONTROL Y VALIDACIÓN DE INTEGRIDAD REFERENCIAL
-- Objetivo: Detectar empleados sin registro asociado en la dimensión demográfica.
-- Nota: Si esta consulta devuelve filas, esos roles no existen en dim_jobs_new y debes 
-- agregarlos antes de ejecutar la inserción.
-- ====================================================================================

SELECT 
    e.employee_number        -- Extrae el número único de nómina del empleado
FROM 
    employee_master_data AS e -- Tabla maestra origen con los datos de empleados
LEFT JOIN 
    dim_demographics AS d    -- Une con dimensión demográfica por id de empleado
    ON e.employee_number = d.employee_number -- Coincidencia por número de nómina
WHERE 
    d.sk_demographics_id IS NULL; -- Filtra colaboradores no registrados en la dimensión