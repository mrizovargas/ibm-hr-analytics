/*******************************************************************************
 * Título: Análisis de riesgos en consultas sin filtro relacional
 * 
 * Objetivo: Ilustrar el problema del 'Producto Cartesiano' en bases de datos.
 * 
 * Descripción: Muestra el resultado de combinar tablas sin especificar cómo se 
 * relacionan, lo que genera un error de duplicación masiva de datos.
 *
 *Archivo SQL: day16_risk_unfiltered_employees_jobs.sql
 ******************************************************************************/

-- INICIO DE LA CONSULTA:
-- Seleccionamos el ID del empleado y su puesto de trabajo.
SELECT 
    e.employee_number, 
    j.job_role

-- ORIGEN DE LOS DATOS:
-- Indicamos que extraeremos información de dos fuentes diferentes.
FROM 
	fact_employees AS e, 
	dim_jobs AS j

-- ADVERTENCIA SOBRE EL RIESGO:
-- Este enfoque carece de una condición de unión (como un JOIN). 
-- Al no tener un filtro, la base de datos combina cada empleado con 
-- absolutamente todos los puestos, generando millones de filas por error.
; 
