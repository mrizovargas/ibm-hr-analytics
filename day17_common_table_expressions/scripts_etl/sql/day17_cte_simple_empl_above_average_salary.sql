/*************************************************************************************
 Título: Identificación de empleados con salario superior al promedio general

 Objetivo: Listar los empleados cuyo ingreso mensual supera el promedio global de la 
 empresa.

 Descripción: El script calcula primero el sueldo promedio de toda la organización. 
 Luego, compara cada sueldo individual contra ese promedio, filtrando y ordenando a los 
 empleados con mayores ingresos de forma descendente.

 Archivo SQL: day17_cte_simple_empl_above_average_salary.sql

 Archivo CSV: day17_cte_simple_empl_above_average_salary.csv

  Archivo PNG: day17_cte_simple_empl_above_average_salary.png
*************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CÁLCULO DEL SALARIO PROMEDIO GLOBAL
-- Objetivo: Obtener la media salarial de toda la empresa para usarla como referencia
-- ====================================================================================

-- Definimos una tabla temporal llamada "salario_promedio"
WITH salario_promedio AS (
	SELECT 
		-- Calculamos el promedio de todos los sueldos registrados
		AVG(monthly_income) AS promedio_global
	FROM 
		-- Fuente de datos con la información completa de empleados
		employee_master_data
)

-- ====================================================================================
-- BLOQUE 2: FILTRADO Y ORDENAMIENTO DE EMPLEADOS
-- Objetivo: Consultar datos individuales y filtrar a quienes ganan más del promedio
-- ====================================================================================

SELECT 
	-- Número de identificación único del empleado
	e.employee_number,
	-- Departamento al que pertenece
	e.department,
	-- Puesto o rol laboral que desempeña
	e.job_role,
	-- Sueldo mensual individual
	e.monthly_income,
	-- Redondeamos el promedio global a 2 decimales para que sea fácil de leer
	ROUND(s.promedio_global, 2) AS salario_promedio_empresa

FROM employee_master_data AS e

-- Combinamos la tabla principal con la tabla temporal que contiene el promedio
CROSS JOIN
	salario_promedio AS s

-- Conservamos únicamente a los empleados que ganan más que el promedio global
WHERE
	e.monthly_income > s.promedio_global

-- Ordenamos la lista comenzando por los sueldos más altos
ORDER BY
	e.monthly_income DESC;