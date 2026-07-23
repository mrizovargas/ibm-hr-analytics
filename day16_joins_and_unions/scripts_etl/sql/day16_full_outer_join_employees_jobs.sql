/*******************************************************************************
* Título: Unión de empleados y sus puestos de trabajo
* 
* Objetivo: Cruzar dos bases de datos para ver de dónde es cada empleado.
* 
* Descripción: El script toma la lista de empleados y la junta con la lista de 
* puestos de trabajo. Muestra todos los datos de ambos lados, incluso si hay 
* registros que no coinciden o están incompletos.
*
* Archivo SQL: day16_full_outer_join_employees_jobs.sql
*
* Archivo CSV: day16_full_outer_join_employees_jobs.csv
*
* Archivo PNG: day16_full_outer_join_employees_jobs.png
*******************************************************************************/

SELECT 
    e.employee_number,              -- Extraemos el número de identificación del empleado.
    e.monthly_income,               -- Extraemos el salario mensual que gana el empleado.
    j.job_id AS job_id_catalogo,    -- Extraemos el ID del puesto y lo llamamos 'job_id_catalogo'.
    j.job_role,                     -- Extraemos el nombre o título del puesto de trabajo.
    j.department                    -- Extraemos el departamento al que pertenece el puesto.
FROM fact_employees AS e            -- Usamos la tabla de empleados y la llamamos 'e'.
FULL JOIN dim_jobs AS j             -- Unimos todo con la tabla de puestos, llamada 'j'.
    ON e.job_id = j.job_id;         -- Conectamos ambas tablas usando el código de puesto (job_id).
