/*******************************************************************************
Título: Validación de Integridad en Tabla Maestra de Empleados

Objetivo: Verificar si existen registros en la tabla 'employee_master_data' 
para asegurar que hay datos antes de proceder con procesos de ETL, reportes o 
actualizaciones.

Descripción: Este script realiza un conteo rápido de todas las filas existentes 
en la tabla maestra de empleados. Sirve como una comprobación de integridad o 
"sanity check" inicial.

Archivo SQL: day01_sanity check_empl_mstr_tbl.sql

Archivo PNG: day01_sanity check_empl_mstr_tbl.png
********************************************************************************/

-- Valida la existencia del dato con una consulta de conteo
SELECT 
	COUNT(*) AS total_registros
FROM 
	employee_master_data;