/*******************************************************************************
Título: Análisis de Duplicidad de Empleados

Objetivo: Identificar grupos de empleados duplicados en la base de datos.

Descripción: Este script agrupa a los empleados por edad, puesto y departamento 
para detectar combinaciones donde exista más de un registro, lo que sugiere una 
posible duplicidad de información.

Archivo SQL: day04_find_duplicate_empl.sql

Archivo CSV: day04_find_duplicate_empl.csv

Archivo PNG: day04_find_duplicate_empl.png
**********************************************************************************/

SELECT 
    -- Seleccionamos las columnas clave para identificar la duplicidad
    age,                -- Edad del empleado
    job_role,           -- Puesto de trabajo
    department,         -- Departamento al que pertenece
    -- Contamos cuántos empleados hay en cada combinación de las columnas anteriores
    COUNT(employee_number) AS total_registros
FROM 
    -- Tabla principal que contiene los datos maestros de los empleados
    employee_master_data
GROUP BY 
    -- Agrupamos por los campos seleccionados para consolidar los conteos
    age,
    job_role,
    department
HAVING
    -- Filtramos el resultado para mostrar solo los grupos con más de 1 registro (duplicados)
    COUNT(employee_number) > 1;











