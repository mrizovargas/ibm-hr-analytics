/*******************************************************************************
Título: Identificación de Empleados sin Departamento Asignado

Objetivo: Detectar registros de empleados incompletos en la base de datos maestra.

Descripción: Esta consulta selecciona a todos los empleados de la tabla maestra que 
no tienen un departamento asignado (valor nulo), para su posterior revisión y 
actualización.

Archivo SQL: day03_null_audit.sql
 
Archivo PNG: day03_null_audit.png
*******************************************************************************/

-- Selecciona todos los campos (*) para visualizar la información completa del empleado
SELECT * 
-- Desde la tabla maestra de empleados
FROM employee_master_data 
-- Filtra para mostrar solo filas donde la columna 'department' esté vacía (NULL)
WHERE department IS NULL;










