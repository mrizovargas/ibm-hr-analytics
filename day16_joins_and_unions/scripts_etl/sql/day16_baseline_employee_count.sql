/***************************************************************************************
-- Título: Conteo de Línea Base de Empleados
-- 
-- Objetivo: Calcular la cantidad total de registros originales en la tabla de hechos.
-- 
-- Descripción: Este script realiza una operación fundamental de auditoría y control de 
-- datos. Su objetivo es contar cuántos empleados existen en total dentro de la tabla 
-- principal ("fact_employees") antes de realizar cualquier tipo de unión o combinación 
-- futura. El número resultante sirve como nuestra "ancla de validación" o línea base 
-- para asegurar que ningún dato se pierda misteriosamente en reportes posteriores.
-- 
-- Archivo SQL: day16_baseline_employee_count.sql
-- 
-- Archivo CSV: day16_baseline_employee_count.csv
-- 
-- Archivo PNG: day16_baseline_employee_count.png
 ***************************************************************************************/

-- PASO 1: Le pedimos al sistema que cuente todas las filas y le damos un nombre claro.
SELECT COUNT(*) AS total_empleados_originales 

-- PASO 2: Indicamos la fuente original de donde se extraerá este conteo.
FROM fact_employees; -- Buscamos directamente en la tabla principal de empleados.