/**************************************************************************************
 Título: Consulta de Verificación de Índices en PostgreSQL

 Objetivo: Confirmar la existencia de un índice en una columna específica.

 Descripción: Este script inspecciona el catálogo del sistema en PostgreSQL para
 verificar si la tabla 'dim_jobs' tiene un índice asociado a la columna 'job_id'.

 Archivo SQL: day16_check_table_indexes.sql
 
 Archivo PNG: day16_check_table_indexes.png
*****************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: SELECCIÓN DE CAMPOS INFORMATIVOS
-- Objetivo: Elegir las columnas del catálogo que muestran el detalle del índice.
-- ====================================================================================

SELECT 
    schemaname, -- Muestra el esquema de la base de datos al que pertenece la tabla.
    tablename,  -- Indica el nombre exacto de la tabla consultada dentro del sistema.
    indexname,  -- Presenta el nombre con el que se identificó y guardó el índice.
    indexdef    -- Muestra la instrucción técnica completa utilizada para crearlo.

-- ====================================================================================
-- BLOQUE 2: ORIGEN DE LOS DATOS Y FILTRADO
-- Objetivo: Consultar la tabla del sistema y aplicar los criterios de búsqueda.
-- ====================================================================================

FROM pg_catalog.pg_indexes         -- Consultamos la vista que guarda todos los índices.
WHERE tablename = 'dim_jobs'       -- Limitamos la búsqueda a la tabla de puestos.
  AND indexdef LIKE '%job_id%';    -- Confirmamos si la columna 'job_id' está indexada.