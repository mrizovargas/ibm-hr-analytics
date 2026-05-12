/*******************************************************************************
Título: Identificación de Aumentos Salariales Atípicos

Objetivo: Detectar empleados con aumentos salariales porcentuales fuera del rango 
estándar.

Descripción: Esta consulta selecciona empleados cuyos aumentos (percent_salary_hike) 
son muy bajos (< 11%) o muy altos (> 25%), útil para auditorías o revisiones de 
compensación.

Archivo SQL: day04_audit_atypical_salary_hikes.sql

Archivo CSV: day04_audit_atypical_salary_hikes.csv

Archivo PNG: day04_audit_atypical_salary_hikes.png
*********************************************************************************/

-- Iniciamos la selección de los datos específicos que necesitamos consultar
SELECT 
    employee_number,      -- Identificador único del trabajador
    percent_salary_hike   -- El porcentaje de aumento salarial aplicado
FROM 
    employee_master_data  -- De nuestra base de datos principal de empleados
WHERE 
    -- Filtramos para encontrar solo los casos excepcionales:
    percent_salary_hike < 11   -- Aquellos que recibieron menos del 11% (incrementos bajos)
    OR                         -- O bien...
    percent_salary_hike > 25;  -- Aquellos que superaron el 25% (incrementos altos)