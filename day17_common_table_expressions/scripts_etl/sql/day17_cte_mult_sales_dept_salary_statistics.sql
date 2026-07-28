/*************************************************************************************
 Título: Análisis estadístico de salarios en el departamento de ventas

 Objetivo: Calcular métricas clave de ingresos por rol dentro del área de ventas.

 Descripción: Primero, el script filtra a todo el personal del departamento de ventas. 
 Después, agrupa esta información por rol de trabajo para calcular la cantidad de 
 empleados, así como el salario promedio, mínimo y máximo de cada puesto. Finalmente, 
 presenta los resultados ordenados del sueldo promedio más alto al más bajo.

 Archivo SQL: day17_cte_mult_sales_dept_salary_statistics.sql

 Archivo CSV: day17_cte_mult_sales_dept_salary_statistics.csv

 Archivo PNG: day17_cte_mult_sales_dept_salary_statistics.png
*************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: FILTRADO DE EMPLEADOS DE VENTAS
-- Objetivo: Aislar la información del personal perteneciente al departamento de Ventas
-- ====================================================================================

-- Creamos la primera vista temporal con el grupo de trabajo de ventas
WITH empleados_ventas AS (
	SELECT 
		-- Identificador único de cada colaborador
		employee_number,
		-- Departamento al que pertenece (Ventas)
		department,
		-- Puesto o rol que desempeña en la empresa
		job_role,
		-- Ingreso o sueldo mensual asignado
		monthly_income
	FROM
		-- Tabla principal con los datos maestros de personal
		employee_master_data
	WHERE
		-- Seleccionamos únicamente al equipo de Ventas
		department = 'Sales'
),

-- ====================================================================================
-- BLOQUE 2: CÁLCULO DE ESTADÍSTICAS POR PUESTO
-- Objetivo: Agrupar por rol y obtener conteo, promedio, mínimo y máximo de ingresos
-- ====================================================================================

-- Creamos la segunda vista temporal para consolidar los indicadores por rol
estadisticas_ventas AS (
	SELECT
		-- Nombre del puesto evaluado
		job_role,
		-- Contamos cuántas personas ocupan este puesto
		COUNT(employee_number) AS cantidad_empleados,
		-- Obtenemos el sueldo promedio del puesto redondeado a dos decimales
		ROUND(AVG(monthly_income), 2) AS salario_promedio_rol,
		-- Obtenemos el sueldo más bajo del puesto
		MIN(monthly_income) AS salario_minimo_rol,
		-- Obtenemos el sueldo más alto del puesto
		MAX(monthly_income) AS salario_maximo_rol
	FROM
		-- Usamos los datos previamente filtrados del equipo de ventas
		empleados_ventas
	GROUP BY 
		-- Agrupamos los cálculos para cada rol de trabajo distinto
		job_role
)

-- ====================================================================================
-- BLOQUE 3: CONSULTA FINAL Y ORDENAMIENTO DE RESULTADOS
-- Objetivo: Mostrar el resumen salarial por rol de mayor a menor sueldo promedio
-- ====================================================================================

SELECT
	-- Presentamos el rol laboral
	job_role,
	-- Total de personal en ese rol
	cantidad_empleados,
	-- Sueldo promedio calculado
	salario_promedio_rol,
	-- Sueldo más bajo en el rol
	salario_minimo_rol,
	-- Sueldo más alto en el rol
	salario_maximo_rol
FROM 
	-- Consultamos la vista temporal con el resumen estadístico
	estadisticas_ventas
ORDER BY 
	-- Ordenamos la lista comenzando por el puesto con mayor promedio salarial
	salario_promedio_rol DESC;