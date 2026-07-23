/**************************************************************************************
 Título: Detección de IDs de Trabajos Duplicados

 Objetivo: Identificar qué códigos de trabajo se encuentran repetidos en la tabla.

 Descripción: El script analiza la tabla de trabajos, agrupa los registros por su ID y 
 cuenta cuántas veces aparece cada uno. Finalmente, filtra la lista para mostrar solo 
 los casos con más de una aparición.

 Archivo SQL: day16_find_duplicate_jobs.sql

 Archivo PNG: day16_find_duplicate_jobs.png
**************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: BÚSQUEDA Y FILTRADO DE TRABAJOS DUPLICADOS
-- Objetivo: Agrupar la información por trabajo y conservar solo los registros repetidos
-- ====================================================================================

-- Definimos las columnas a mostrar: el código del trabajo y el total de apariciones
SELECT 
	job_id,
	COUNT(*)

-- Especificamos el origen de los datos (la tabla principal de trabajos)
FROM dim_jobs

-- Organizamos toda la lista reuniendo todos los registros que comparten el mismo ID
GROUP BY job_id

-- Filtramos el resultado final para quedarnos únicamente con los IDs repetidos (> 1)
	HAVING COUNT(*) > 1;