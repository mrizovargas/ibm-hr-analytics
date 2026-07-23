/*******************************************************************************
 * Título: Análisis de Empleados en Ventas (Pérdida de Datos)
 * 
 * Objetivo: Rescatar empleados de ventas verificando el comportamiento del 
 * código.
 * 
 * Descripción: Script que intenta buscar empleados del departamento de ventas. 
 * Demuestra el error de usar filtros WHERE sobre uniones LEFT JOIN, lo que 
 * elimina sin querer a los empleados sin puesto asignado.
 * 
 * Archivo SQL: day16_sales_employees_data_missing.sql
 *
 * Archivo PNG: day16_sales_employees_data_missing.png
 ******************************************************************************/

-- Aproximación Incorrecta (Pérdida de Datos)
-- ¡CUIDADO! Esto elimina a los empleados desalineados (los que no tienen departamento)
SELECT
	e.employee_number, -- Extrae el número de identificación del empleado
	d.department       -- Extrae el nombre del departamento asignado
FROM fact_employees AS e -- Toma la tabla principal de empleados y la llama "e"
LEFT JOIN dim_jobs AS d  -- Vincula la tabla de puestos, permitiendo que existan empleados sin puesto
	ON e.job_id = d.job_id -- Conecta ambas tablas usando el código o ID del puesto
WHERE 
	d.department = 'Sales'; -- Filtra para que solo veamos a los empleados en Ventas
-- El WHERE destruye los valores NULL (vacíos) del LEFT JOIN, descartando empleados sin puesto asignado
