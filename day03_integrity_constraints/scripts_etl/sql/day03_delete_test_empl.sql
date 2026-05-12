/*******************************************************************************
Título: Depuración de Maestros de Empleados

Objetivo: Eliminar registros de prueba o incorrectos.

Descripción: Este script borra de la tabla 'employee_master_data' a todos los 
empleados cuyo número de empleado sea 8888 o superior, ya que estos suelen 
corresponder a datos de prueba no reales.

Archivo SQL: day03_delete_test_empl.sql

Archivo PNG: day03_delete_test_empl.png
*******************************************************************************/

-- Se inicia la acción de borrado en la tabla maestra de empleados
DELETE FROM 
	employee_master_data
-- Se establece la condición para identificar solo a los empleados con ID 8888 o mayor
WHERE 
	employee_number >= 8888;











