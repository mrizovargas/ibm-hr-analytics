/*******************************************************************************
Título: Consulta y Ranking de Deserción Laboral (Attrition Rate)

Objetivo: Identificar y ordenar las áreas con mayor rotación de personal.

Descripción: Este script extrae la información completa de la vista base de 
deserción y la ordena de mayor a menor según el porcentaje. El fin es detectar 
rápidamente los "focos rojos" o departamentos con mayor pérdida de talento.

Archivo SQL: day12_get_attrition_rate_ranking.sql

Archivo CSV: day12_get_attrition_rate_ranking.csv

Archivo PNG: day12_get_attrition_rate_ranking.png
**********************************************************************************/

-- 1. SELECCIÓN DE INFORMACIÓN (Lectura de datos)
-- El asterisco (*) indica que queremos traer todas las columnas y métricas 
-- disponibles en la fuente (como el total de empleados, bajas y el porcentaje).
SELECT *

-- 2. ORIGEN DE LOS DATOS
-- Especificamos que la información se va a leer desde la vista virtual 
-- que calcula la tasa base de deserción.
FROM
	view_attrition_rate_base

-- 3. ORDENAMIENTO DE LOS RESULTADOS (Bloque de organización)
-- Organizamos la lista basándonos en la columna del porcentaje de deserción ('raw_attrition_rate').
-- La palabra 'DESC' (Descendente) asegura que los porcentajes más altos aparezcan 
-- primero, facilitando ver qué áreas requieren atención urgente.
ORDER BY 
	raw_attrition_rate DESC;