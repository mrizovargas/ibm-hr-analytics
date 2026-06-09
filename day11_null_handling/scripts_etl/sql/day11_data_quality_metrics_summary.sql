/*******************************************************************************
Título: Reporte Métrico de Datos Homologados (Manejo de Nulos)

Objetivo: Cuantificar cuántos datos vacíos fueron corregidos por la vista de 
limpieza.

Descripción: Este script genera un resumen estadístico para la auditoría de datos. 
Su función es contar el universo total de empleados y medir el impacto exacto de 
nuestras reglas de negocio. Para ello, cuenta cuántas filas tuvieron que ser 
corregidas cambiando su salario vacío por un cero (0) y cuántas evaluaciones 
faltantes se marcaron bajo el código especial de control (99).

Archivo SQL: day11_data_quality_metrics_summary.sql

Archivo CSV: day11_data_quality_metrics_summary.csv

Archivo PNG: day11_data_quality_metrics_summary.png
*********************************************************************************/

-- BLOQUE DE MÉTRICAS Y AGREGACIÓN: Calcula los indicadores clave de calidad de datos.
SELECT
	-- Cuenta el total absoluto de empleados registrados en la base de datos.
	COUNT(*) AS total_registros,
    
	-- Filtro y Suma de Ingresos: Analiza fila por fila. Si el ingreso limpio es 0, 
	-- le asigna un 1 (si no, un 0) y al final suma todos los unos. 
	-- Esto nos da el total exacto de salarios que estaban vacíos y fueron corregidos.
	SUM(CASE WHEN clean_monthly_income = 0 THEN 1 ELSE 0 END) AS ingresos_reemplazados_con_cero,
    
	-- Filtro y Suma de Evaluaciones: Aplica la misma lógica. Si encuentra el código 
	-- de control 99, cuenta un 1. Al sumarlos, sabemos cuántos empleados no tenían 
	-- una calificación real en el sistema.
	SUM(CASE WHEN clean_performance_rating = 99 THEN 1 ELSE 0 END) AS evaluaciones_marcadas_sin_evaluar

-- BLOQUE DE ORIGEN: Especifica la fuente de los datos para el reporte.
FROM
	-- Consultamos la vista estandarizada donde ya se aplicó el reemplazo de nulos.
	view_clean_null_handling;