/*==============================================================================
Título: Análisis y Optimización de Búsqueda de Empleados

Objetivo: Identificar y optimizar la consulta de empleados de Investigación y 
Desarrollo (R&D) que han renunciado.

Descripción: El script evalúa el tiempo que toma buscar datos clave (número, 
puesto e ingreso) de empleados específicos. Luego, crea una "guía rápida" (índice) 
para acelerar esta búsqueda y vuelve a medir el tiempo para confirmar la mejora.

Archivo SQL: day08_idx_employee_search_optimization.sql

Archivo CSV: day08_idx_employee_search_optimization.csv

Archivo PNG: day08_idx_employee_search_optimization_01.png
             day08_idx_employee_search_optimization_02.png
             day08_idx_employee_search_optimization_03.png
==============================================================================*/

/*==============================================================================
PASO A: Diagnóstico inicial (Sin optimización)
==============================================================================*/
-- Evalúa y ejecuta la consulta para encontrar los empleados de R&D que renunciaron.
EXPLAIN ANALYZE 
SELECT 
	employee_number, 
	job_role, 
	monthly_income 
FROM 
	employee_master_data 
WHERE 
	department = 'Research & Development' 
	AND attrition = 'Yes';

/*==============================================================================
PASO B: Creación de la mejora (Índice)
==============================================================================*/
-- Crea una estructura de búsqueda rápida (índice) combinando el departamento y la 
-- condición de renuncia. Esto evita que el sistema tenga que leer toda la base de 
-- datos desde cero la próxima vez.
CREATE INDEX idx_employee_dept_attrition 
ON employee_master_data(department, attrition);

/*==============================================================================
PASO C: Diagnóstico final (Con optimización)
==============================================================================*/
-- Vuelve a ejecutar la misma consulta del Paso A para medir y comprobar 
-- cuánto más rápido responde el sistema ahora que cuenta con el índice creado.
EXPLAIN ANALYZE 
SELECT 
	employee_number, 
	job_role, 
	monthly_income 
FROM 
	employee_master_data 
WHERE 
	department = 'Research & Development' 
	AND attrition = 'Yes';
