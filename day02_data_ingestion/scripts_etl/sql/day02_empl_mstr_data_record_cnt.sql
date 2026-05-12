/*******************************************************************************
Título: Verificación de Carga de Datos de RRHH

Objetivo: Contabilizar el total de registros en la tabla 'employee_master_data'.

Descripción: Este comando nos permite confirmar cuántos empleados se han cargado 
exitosamente en la base de datos tras ejecutar el pipeline.

Archivo SQL: day02_empl_mstr_data_record_cnt.sql

Archivo PNG: day02_empl_mstr_data_record_cnt.png
********************************************************************************/

-- ---------------------------------------------------------
-- 1. Consulta de conteo total
-- ---------------------------------------------------------

SELECT
    -- Cuenta el número total de filas o registros existentes
	COUNT(*)
FROM
    -- Indica la tabla específica donde está guardada la información de los empleados
	employee_master_data;

