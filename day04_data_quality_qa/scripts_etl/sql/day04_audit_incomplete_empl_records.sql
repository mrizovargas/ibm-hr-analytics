/*******************************************************************************
Título: Auditoría de Datos Maestros de Empleados - Registros Incompletos

Objetivo: Identificar la cantidad de empleados que tienen información faltante 
crítica en sus registros.

Descripción: Este script cuenta cuántos registros en la tabla 'employee_master_data' 
tienen el departamento vacío, el rol de trabajo vacío o el campo de educación nulo, 
lo que permite medir la calidad de los datos.

Archivo SQL: day04_audit_incomplete_empl_records.sql

Archivo CSV: day04_audit_incomplete_empl_records.csv

Archivo PNG: day04_audit_incomplete_empl_records.png
*********************************************************************************/

-- Selecciona el conteo total de filas que cumplen los criterios de búsqueda
SELECT 
    COUNT(*)
FROM 
    employee_master_dirty_data -- Tabla principal de datos maestros de empleados
WHERE 
    -- Filtro 1: Busca registros donde el departamento esté vacío (cadena vacía)
    department = ''
    -- Filtro 2: O busca registros donde el rol de trabajo esté vacío (cadena vacía)
    OR job_role = ''
    -- Filtro 3: O busca registros donde el campo de educación sea explícitamente nulo (NULL)
    OR education_field IS NULL;