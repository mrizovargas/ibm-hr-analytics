/*******************************************************************************
Título: Creación de Vista Maestra: Tasa de Deserción por Puesto y Área

Objetivo: Centralizar y calcular de forma segura el porcentaje de bajas de 
personal.

Descripción: Este script genera una estructura virtual (Vista) que calcula de 
manera automática el total de empleados, las bajas confirmadas y la tasa de 
deserción porcentual, protegiendo la operación contra errores de división por 
cero si un puesto se queda sin personal.

Archivo SQL: day12_create_view_attrition_rate_base.sql

Archivo PNG: day12_view_attrition_rate_base.png
************************************************************************************/

-- 1. CREACIÓN DE LA ESTRUCTURA VIRTUAL (VISTA)
-- Si la vista ya existía, la actualiza con los nuevos cambios sin borrar los datos reales.
CREATE OR REPLACE VIEW view_attrition_rate_base AS 
	
	-- 2. SELECCIÓN Y PROCESAMIENTO DE MÉTRICAS (Bloque Principal)
	SELECT
		department, -- Departamento del empleado.
		job_role,   -- Puesto o rol de trabajo.
		
		-- CONTEO DE PERSONAL: Cuenta los identificadores únicos para saber cuánta gente hay en total.
		COUNT(employee_number) AS total_headcount,
		
		-- CONTADOR DE BAJAS: Revisa el estatus; si dice 'Yes', le asigna un 1, si no, un 0, y luego los suma.
		SUM(CASE WHEN (attrition) = 'Yes' THEN 1 ELSE 0 END) AS total_bajas,
		
		-- CÁLCULO DE LA TASA DE DESERCIÓN PROTEGIDA:
		-- Tomamos el total de bajas y lo multiplicamos por 100 para preparar el formato de porcentaje.
		-- Usamos NULLIF en el divisor para que, si el conteo de empleados es 0, se transforme en NULL.
		-- De esta forma, la división devuelve un valor vacío seguro en lugar de romper el sistema.
		-- Finalmente, ROUND(..., 2) redondea el porcentaje resultante a sólo 2 decimales.
		ROUND(
			(SUM(CASE WHEN (attrition) = 'Yes' THEN 1 ELSE 0 END) * 100) /
			NULLIF(COUNT(employee_number), 0), 2
		) AS raw_attrition_rate

	-- 3. ORIGEN DE LOS DATOS
	-- Indicamos la tabla de la cual se va a extraer todo el histórico del personal.
	FROM
		employee_master_data
		
	-- 4. AGRUPACIÓN Y ORDEN DE LA INFORMACIÓN
	-- Divide los cálculos anteriores para obtener métricas individuales por cada Departamento y Puesto.
	GROUP BY
		department,
		job_role
	-- Organiza el resultado final alfabéticamente por el nombre del departamento.
	ORDER BY
		department;