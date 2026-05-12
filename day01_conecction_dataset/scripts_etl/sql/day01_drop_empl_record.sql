/*******************************************************************************
Título: Eliminación de Registro de Empleado

Objetivo: Depurar la tabla maestra de empleados.

Descripción: Este script elimina un registro específico de la tabla 'employee_master_data' 
utilizando el número de empleado como identificador único para mantener la base de datos actualizada.

Archivo SQL: day01_drop_empl_record.sql

Archivo PNG: day01_drop_empl_record.png
*******************************************************************************/

-- Bloque lógico: Eliminación segura de registro
-- Se utiliza la cláusula WHERE para asegurar que solo se borre el empleado 
-- con el número 9999 y no toda la tabla.
DELETE FROM 
    employee_master_data  -- Define la tabla de la cual se borrarán los datos
WHERE 
	employee_number = 9999; -- Especifica la condición única del registro a eliminar