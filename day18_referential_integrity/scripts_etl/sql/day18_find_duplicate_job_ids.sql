/*******************************************************************************
 Título: Identificación de identificadores de puestos duplicados.

 Objetivo: Detectar cuáles valores de 'job_id' aparecen más de una vez en la 
 tabla.

 Descripción: Agrupa los registros por 'job_id', cuenta las ocurrencias de cada 
 uno y filtra únicamente los grupos cuya cuenta sea mayor a 1.

 Archivo SQL: day18_find_duplicate_job_ids.sql

 Archivo PNG: day18_find_duplicate_job_ids_flowchart.png

*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: Consulta de detección de registros duplicados
-- Objetivo: Agrupar por ID y filtrar aquellos que se repiten en la tabla
-- ====================================================================================

-- Paso 1: Seleccionamos el ID y agregamos un contador de ocurrencias
SELECT 
	job_id,                      -- Muestra el identificador del puesto
	COUNT(*) AS total_registros  -- Cuenta cuántas veces aparece ese ID

-- Paso 2: Especificamos la tabla de origen
FROM dim_jobs

-- Paso 3: Agrupamos las filas que comparten el mismo 'job_id'
GROUP BY job_id

-- Paso 4: Filtramos para mostrar solo registros duplicados (más de 1) o nulos
HAVING COUNT(*) > 1
	OR job_id IS NULL;