/*******************************************************************************
Título: Análisis de Distribución de Empleados por Segmento de Riesgo

Objetivo: Identificar cuántos empleados pertenecen a cada categoría de riesgo.

Descripción: El script agrupa al personal según su segmento de riesgo de fuga,
calcula el volumen total por grupo y determina qué porcentaje representa cada 
segmento sobre el total de la empresa.

Archivo SQL: day10_empl_talent_risk_segmentation.sql

Archivo CSV: day10_empl_talent_risk_segmentation.csv

Archivo PNG: day10_empl_talent_risk_segmentation.png
*********************************************************************************/

-- Bloque 1: Selección de campos y cálculo de métricas de distribución
SELECT
	-- Identifica la categoría de riesgo del empleado
	risk_segment,
	
	-- Cuenta el número total de empleados en cada categoría
	COUNT(*) AS total_empleados,
	
	-- Calcula el porcentaje que representa cada grupo sobre el total global de la empresa
	ROUND(COUNT(*)*100.0 / SUM(COUNT(*)) OVER(),2) AS porcentaje_distribucion

-- Bloque 2: Origen de los datos
FROM view_talent_risk_satisfaction

-- Bloque 3: Agrupación y ordenamiento del reporte
-- Agrupa los resultados por cada tipo de segmento de riesgo
GROUP BY risk_segment

-- Muestra primero los segmentos con mayor volumen de empleados
ORDER BY total_empleados DESC;