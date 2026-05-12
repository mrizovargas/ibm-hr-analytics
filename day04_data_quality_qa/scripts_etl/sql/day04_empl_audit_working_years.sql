/*******************************************************************************
 Título: Auditoría de Coherencia en Experiencia Laboral
 
 Objetivo: Identificar registros de empleados con datos inconsistentes.
 
 Descripción: Selecciona empleados cuya experiencia laboral total sea lógica 
 o físicamente imposible en relación con su edad actual (ej. más años de trabajo 
 que años de vida menos la mayoría de edad).

Archivo SQL: day04_empl_audit_working_years.sql

Archivo CSV: day04_empl_audit_working_years.csv

Archivo PNG: day04_empl_audit_working_years.png
**********************************************************************************/

SELECT 
    employee_number,     -- Identificador único del empleado
    age,                 -- Edad actual del empleado
    total_working_years, -- Años totales de experiencia reportados
    job_role             -- Puesto de trabajo actual
FROM 
    employee_master_data -- Tabla fuente con los datos maestros de empleados
WHERE 
    -- Filtro de lógica: Selecciona si la experiencia es mayor a la edad 
    -- menos 18 años (asumiendo que no trabajan antes de los 18).
    -- Ejemplo: 19 años de edad - 18 = Máximo 1 año de experiencia lógica.
    age < (total_working_years + 18);













