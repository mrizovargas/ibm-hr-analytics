/*******************************************************************************
* Título: Cruce de Empleados y Departamentos
* 
* Objetivo: Generar un listado que relacione a cada empleado con todos los 
* posibles departamentos de la empresa.
* 
* Descripción: El script toma la información base de los empleados (número e 
* ingresos) y las combina con una lista única de departamentos. Esto crea todas 
* las parejas o combinaciones posibles entre el personal y las áreas de trabajo.
*
* Archivo SQL: day16_employee_department_cross_join.sql
*
* Archivo PNG: day16_employee_department_cross_join.png
*******************************************************************************/

SELECT 
    e.employee_number, -- Extrae el número de identificación único del empleado
    e.monthly_income,  -- Extrae el valor del ingreso mensual de dicho empleado
    d.department       -- Extrae el nombre del departamento
FROM fact_employees AS e
CROSS JOIN (           -- Une cada empleado con TODOS los registros de la otra tabla
    SELECT DISTINCT department -- Extrae solo los nombres de departamento únicos, sin repetir
    FROM dim_jobs      -- Tabla que contiene la información de los puestos y áreas
) AS d;                -- Nombra temporalmente a esta lista de departamentos como 'd'
