/*******************************************************************************
Título: Consulta de Departamentos Únicos

Objetivo: Obtener una lista depurada de todos los departamentos existentes.

Descripción: Este script consulta la tabla maestra de empleados para extraer la 
lista de departamentos, eliminando duplicados para obtener una lista única y 
ordenada de las áreas de la empresa.

Archivo SQL: day04_get_unique_departments.sql

Archivo CSV: day04_get_unique_departments.csv

Archivo PNG: day04_get_unique_departments.png
*********************************************************************************/

-- Selecciona valores únicos (sin duplicados) de la columna departamento
SELECT DISTINCT department
-- Indica que la información se obtiene de la tabla maestra de empleados
FROM 
	employee_master_dirty_data;