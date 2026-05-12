/*******************************************************************************
Título: Eliminación de Empleado Específico

Objetivo: Dar de baja a un empleado de la base de datos maestra.

Descripción: Esta sentencia elimina el registro de un empleado específico de la 
tabla 'employee_master_data' basándose en su número único de empleado.

Archivo SQL: day05_delete_employee_record.sql

Archivo PNG: day05_delete_employee_record.png
*********************************************************************************/

-- Procedemos a eliminar el registro del empleado con número 10
DELETE FROM employee_master_data
WHERE employee_number = 10;
-- 1. DELETE FROM: Indica la tabla de la cual se borrarán los datos.
-- 2. WHERE: Cláusula crucial para filtrar y eliminar SOLO al empleado 10,
--    evitando borrar toda la tabla.