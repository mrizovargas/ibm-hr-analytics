/*******************************************************************************
Título: Identificación de Estados de Rotación (Attrition)

Objetivo: Obtener una lista única de los valores posibles en la columna de rotación 
para entender cómo se categoriza a los empleados.

Descripción: Esta consulta escanea la tabla maestra de empleados y devuelve todos 
los valores distintos presentes en la columna 'attrition' (ej. "Yes", "No", 
"Voluntary", "Involuntary"), eliminando duplicados.

Archivo SQL: day03_domain_audit.sql

Archivo PNG: day03_domain_audit.png
*********************************************************************************/

-- Selecciona valores únicos (sin duplicados)
SELECT DISTINCT 
    attrition -- Columna que indica si el empleado ha dejado la empresa
FROM
    employee_master_data; -- Tabla origen con la información general del empleado











