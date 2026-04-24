/*******************************************************************************
Título: Reporte de Empleados con Alto Ingreso y Baja Satisfacción.

Objetivo: Identificar empleados con salarios superiores a 5,000 que reportan 
una baja satisfacción laboral (menor a 2), para análisis de retención.

Descripción: Este script cruza datos de empleados con catálogos de departamentos 
y puestos, filtrando por ingresos y satisfacción, y ordenando de mayor a menor sueldo.

Resultado CSV: day02_hr_risk_analysis_results.csv
*******************************************************************************/


SELECT
	e.employee_number,       -- Número único del empleado
	dc.department_name,       -- Nombre del departamento al que pertenece
	jrc.job_role_name,         -- Nombre del puesto o rol laboral
	e.monthly_income-- Sueldo mensual del empleado
FROM
	employee_final AS e-- Tabla principal de empleados (alias 'e')
JOIN
	department_catalog AS dc-- Une tabla de departamentos (alias 'd')
	ON e.department_id = dc.department_id-- Conexión por ID de departamento
JOIN
	job_role_catalog AS jrc-- Une tabla de puestos (alias 'j')
	ON e.job_role_id = jrc.job_role_id-- Conexión por ID de puesto
WHERE
	e.monthly_income > 5000-- Filtro 1: Empleados que ganan más de 5,000
	AND e.job_satisfaction < 2-- Filtro 2: Empleados con bajo nivel de satisfacción (escala 1-4)
ORDER BY
	e.monthly_income DESC;-- Ordena el resultado del sueldo más alto al más bajo



/*******************************************************************************
Título: Reporte de Promedio de Ingresos por Departamento

Objetivo: Calcular y visualizar el salario mensual promedio de los empleados 
agrupados por departamento, ordenados del mayor al menor.

Descripción: Este script combina la información de empleados y departamentos, 
realiza el cálculo del promedio y ordena el resultado para identificar 
fácilmente los departamentos con mayor remuneración promedio.

Resultado CSV: day02_avg_income_by_dept.csv
********************************************************************************/

-- Selecciona el nombre del departamento y calcula el promedio de ingresos mensuales
SELECT
	dc.department_name, 
	-- Calcula el promedio de ingresos (monthly_income) y lo redondea a 2 decimales para mejor lectura
	ROUND(AVG(e.monthly_income),2) AS avg_income
-- Utiliza la tabla de empleados como fuente principal (alias 'e')
FROM
	employee_final e
-- Une con la tabla de catálogo de departamentos (alias 'd') usando el ID compartido
JOIN
	department_catalog AS dc 
	ON e.department_id = dc.department_id
-- Agrupa los resultados para que el promedio se calcule por cada departamento
GROUP BY
	dc.department_name
-- Ordena el reporte final de mayor a menor según el ingreso promedio calculado
ORDER BY
	avg_income DESC;



/*******************************************************************************
Título: Detección de Registros Duplicados de Empleados

Objetivo: Identificar qué empleados aparecen más de una vez en la base de datos.

Descripción: Este script analiza la tabla 'employee_final' para encontrar 
números de empleado (employee_number) que están duplicados, 
lo cual puede indicar errores de carga o datos redundantes.

Resultado CSV: day02_duplicated_empl_records_cnt.csv
*******************************************************************************/

-- 1. Selecciona el número de empleado y cuenta cuántas veces aparece cada uno.
SELECT
	e.employee_number, 
	COUNT(*) AS total_apariciones
FROM
	employee_final AS e-- 2. Especifica la tabla maestra de empleados a consultar.
GROUP BY
	e.employee_number-- 3. Agrupa los resultados por el número de empleado.
HAVING
	COUNT(*) > 1;-- 4. Filtra para mostrar solo los empleados con más de un registro (duplicados).