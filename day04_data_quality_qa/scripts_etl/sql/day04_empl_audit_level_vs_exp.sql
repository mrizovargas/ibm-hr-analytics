/*******************************************************************************
Título: Detección de Anomalías en Nivel y Experiencia (Auditoría de Nómina)

Objetivo: Identificar empleados con alto nivel jerárquico pero poca experiencia.

Descripción: Selecciona colaboradores de nivel 5 (alto) que tienen menos de 10 
años de experiencia total. Esto sirve para detectar errores de captura, posibles 
sesgos en contrataciones o casos excepcionales que requieren revisión de su alto 
ingreso mensual.

Archivo SQL: day04_empl_audit_level_vs_exp.sql

Archivo CSV: day04_empl_audit_level_vs_exp.csv

Archivo PNG: day04_empl_audit_level_vs_exp.png
*********************************************************************************/

-- Seleccionamos los campos clave para auditar al empleado y su relación de ingresos
SELECT 
    employee_number,       -- Identificador único del empleado
    job_level,             -- Nivel jerárquico (se busca nivel 5)
    total_working_years,   -- Años de experiencia total (se busca < 10)
    monthly_income         -- Salario mensual para validar el costo
FROM 
    employee_master_dirty_data   -- Tabla principal de datos maestros del personal
WHERE 
    -- Filtro de alto nivel (5) y baja experiencia (< 10 años)
    job_level = 5 
    AND total_working_years < 10;                

-- Nota técnica: La relación JobLevel/Experiencia es el cruce crítico, no solo el nivel alto.












