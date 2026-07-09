/*********************************************************************************
 * Título: Resumen de Rotación y Salarios por Departamento
 * 
 * Objetivo: Crear una vista que unifique métricas clave de personal por 
 * departamento.
 * 
 * Descripción: Este script automatiza un reporte para el área de Recursos Humanos. 
 * Su meta es calcular tres indicadores esenciales por cada departamento: el volumen
 * total de empleados que han pasado por la empresa, la cantidad de personas que se 
 * han dado de baja ('attrition') y el salario mensual promedio. Al guardarlo como 
 * una vista, los datos se mantendrán actualizados para futuras consultas sin 
 * necesidad de reescribir todo el código.
 * Archivo SQL: day13_view_attrition_summary.sql
 * 
 * Archivo CSV: day13_view_attrition_summary.csv
 * 
 * Archivo PNG: day13_view_attrition_summary.png
 **********************************************************************************/

-- Si la vista ya existía, la borra y la vuelve a crear con los cambios más recientes.
CREATE OR REPLACE VIEW view_attrition_summary AS
	SELECT
		-- Identifica el departamento evaluado (ej. Ventas, Ingeniería).
		department AS departamento,
		
		-- Cuenta a todo el personal (activos e inactivos) que registra el área.
		COUNT(*) AS total_historico_empleados,
		
		-- Suma 1 cada vez que encuentra un 'Yes' en bajas. Si es 'No', suma 0.
		SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS total_bajas,
		
		-- Calcula el sueldo promedio mensual y lo redondea a dos decimales.
		ROUND(AVG(monthly_income), 2) AS ingreso_mesual_promedio
	FROM
		-- Indica la tabla principal que contiene el historial de los empleados.
		employee_master_data
	GROUP BY
		-- Agrupa los resultados para que las métricas se dividan por cada departamento.
		department;