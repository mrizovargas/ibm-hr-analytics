/*******************************************************************************
Título: Detección de Inconsistencias en Antigüedad Laboral

Objetivo: Identificar registros de empleados con datos erróneos.

Descripción: Selecciona empleados cuya antigüedad en la empresa actual es mayor 
que sus años totales de experiencia laboral, lo cual es lógicamente incorrecto 
(un empleado no puede llevar más años en la empresa que el total de años que ha 
trabajado en su vida).

Archivo SQL: day04_audit_seniority.sql

Archivo CSV: day04_audit_seniority.csv

Archivo PNG: day04_audit_seniority.png
********************************************************************************/

-- Seleccionamos los campos clave para identificar al empleado y revisar sus datos
SELECT 
    employee_number,      -- Identificador único del empleado
    years_at_company,     -- Años en la empresa actual
    total_working_years   -- Años totales de experiencia laboral
FROM
    employee_master_dirty_data  -- Tabla maestra de datos de empleados
WHERE 
    -- Filtramos inconsistencias: Años empresa > Años totales
    years_at_company > total_working_years;