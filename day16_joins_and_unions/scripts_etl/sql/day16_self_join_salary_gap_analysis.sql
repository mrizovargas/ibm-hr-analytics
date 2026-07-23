/*********************************************************************************
 * Título: Comparación de Salarios entre Empleados y sus Jefes
 * 
 * Objetivo: Calcular la diferencia de sueldo de cada trabajador frente a su jefe.
 * 
 * Descripción: Une la tabla de empleados consigo misma para comparar el salario 
 * mensual de un empleado (e) con el de su respectivo gerente (m).
 *
 * Archivo SQL: day16_self_join_salary_gap_analysis.sql
 *********************************************************************************/

SELECT
	-- Muestra el número único que identifica a cada empleado
	e.employee_number AS num_empleado,
	
	-- Muestra cuánto gana el empleado al mes
	e.monthly_income AS salario_empleado,
	
	-- Muestra el número de identificación del jefe del empleado
	m.employee_number AS num_manager,
	
	-- Muestra cuánto gana el jefe del empleado al mes
	m.monthly_income AS salario_manager,
	
	-- Resta el sueldo del empleado al sueldo del jefe para ver la diferencia
	(m.monthly_income - e.monthly_income) AS brecha_salarial

-- Selecciona la tabla principal de donde se obtendrán los datos de empleados
FROM fact_employees AS e

-- Conecta la tabla consigo misma usando el número de jefe como puente
LEFT JOIN fact_employees AS m
	ON e.manager_number = m.employee_number;
