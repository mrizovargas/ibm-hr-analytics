/*******************************************************************************
 Título: Empleados con Sueldo Superior al Promedio de su Propio Departamento

 Objetivo: Identificar empleados cuyo salario supere la media de su área de 
 trabajo.

 Descripción: La consulta utiliza una subconsulta correlacionada para calcular 
 el ingreso promedio específico del departamento de cada empleado y filtra 
 únicamente a aquellos que se encuentran por encima de dicho promedio departamental.

 Archivo SQL: day19_scalsq_emp_above_dept_avg_income.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: Consulta de Empleados con Salario Superior al Promedio Departamental
-- Objetivo: Cruzar tablas y comparar el ingreso de cada empleado vs. su propio departamento
-- ====================================================================================

-- Seleccionamos los datos clave a mostrar: ID del empleado, departamento, rol e ingreso
SELECT 
	f.employee_number,
	d.department,
	d.job_role,
	f.monthly_income

-- Definimos la tabla principal de empleados asignándole el alias "f"
FROM 
	fact_employees AS f

-- Cruzamos con el catálogo de puestos ("d") para obtener el departamento y rol
JOIN dim_jobs AS d 
	ON f.job_id = d.job_id

-- Filtramos para comparar el sueldo del empleado con el promedio de su departamento
WHERE 
	f.monthly_income >(

		-- Subconsulta correlacionada: calcula la media salarial del departamento actual
		SELECT 
			AVG(f2.monthly_income)
		FROM 
			fact_employees AS f2
		JOIN 
			dim_jobs AS d2 ON f2.job_id = d2.job_id
		WHERE 
			d2.department = d.department
	)

-- Ordenamos los resultados por departamento e ingreso en orden descendente
ORDER BY 
	d.department ASC, 
	f.monthly_income DESC;