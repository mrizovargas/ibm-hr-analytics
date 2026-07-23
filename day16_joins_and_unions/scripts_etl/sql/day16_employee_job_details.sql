/**************************************************************************************
 Título: Consulta de Relación de Empleados y Puestos Trabajo

 Objetivo: Obtener la lista de empleados junto con sus roles y departamentos asignados.

 Descripción: Este script combina la tabla principal de empleados con el catálogo de 
 puestos mediante un INNER JOIN para asociar a cada colaborador su rol y área 
 correspondiente.

 Archivo SQL: day16_employee_job_details.sql

 Archivo PNG: day16_employee_job_details.png
***************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: SELECCIÓN DE CAMPOS PRINCIPALES
-- Objetivo: Especificar las columnas requeridas del empleado y de su puesto de trabajo.
-- ====================================================================================

SELECT 
	e.employee_number, -- Número identificador asignado a cada uno de los empleados.
	e.job_id,
	j.job_role,        -- Nombre específico del puesto o rol que desempeña el empleado.
	j.department,       -- Nombre del área o departamento al que pertenece el puesto.
	e.monthly_income

-- ====================================================================================
-- BLOQUE 2: ORIGEN Y COMBINACIÓN DE TABLAS (INNER JOIN)
-- Objetivo: Vincular la tabla de empleados con la de puestos mediante su id común.
-- ====================================================================================

FROM fact_employees AS e   -- Definimos la tabla principal de empleados (alias 'e').

INNER JOIN dim_jobs AS j   -- Unimos la tabla de puestos o catálogo de cargos (alias 'j').
	ON e.job_id = j.job_id; -- Establecemos el cruce utilizando la clave única del puesto.