/*******************************************************************************
 * TÍTULO: Control de Calidad en Cruces de Tablas (QA de Integridad de Datos)
 * 
 * OBJETIVO: Evaluar si un cruce de tablas (LEFT JOIN) conserva todos los datos 
 * originales.
 * 
 * DESCRIPCIÓN:
 * 1. Cuenta el total de empleados en la tabla principal (universo original).
 * 2. Cuenta cuántos registros quedan tras cruzar la tabla de empleados 
 *    con la de puestos, conservando solo aquellos del departamento de 'Sales'.
 * 3. Compara ambos resultados para confirmar si hubo pérdida de datos.
 *
 * Archivo SQL: day_qa_integrity_left_join_sales.sql
 *
 * Archivo PNG: day_qa_integrity_left_join_sales.png
 ******************************************************************************/

-- Bloque 1. Contamos el universo original de la tabla de hechos (Línea Base)
WITH 
conteo_universo_original AS(
	SELECT COUNT(*) AS total_original
	FROM fact_employees
),

-- Bloque 2. Contamos las filas resultantes de tu consulta con LEFT JOIN (Tu Reporte)
conteo_reporte_final AS(
	SELECT COUNT(*) AS total_reporte
	FROM fact_employees AS e
	LEFT JOIN dim_jobs AS d
		ON e.job_id = d.job_id
		AND d.department = 'Sales'
)

-- Bloque 3. Aplicamos la validación matemática (Total Reporte >= Total Original)
SELECT 
	orig.total_original,
	rep.total_reporte,
	-- Calculamos la diferencia de filas entre el reporte final y la base original
	(rep.total_reporte - orig.total_original) AS desviacion_filas,
	-- Emitimos un veredicto: aprobado si el reporte contiene todos los datos originales
	CASE
		WHEN rep.total_reporte >= orig.total_original
			THEN 'APROBADO: El LEFT JOIN mantuvo la integridad del universo original.'
		ELSE 'CRÍTICO: Pérdida silenciosa de datos. Un filtro (posiblemente en el WHERE) alteró el LEFT JOIN.'
	END AS estado_control_calidad
FROM conteo_universo_original AS orig
CROSS JOIN conteo_reporte_final AS rep;
