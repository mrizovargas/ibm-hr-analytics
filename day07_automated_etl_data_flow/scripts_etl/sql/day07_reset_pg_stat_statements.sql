/*******************************************************************************
Título: Limpieza de Estadísticas de Rendimiento
 
Objetivo: Reiniciar los contadores y registros de rendimiento de las consultas SQL 
en PostgreSQL para establecer un "nuevo punto de partida".
 
Descripción: Cuando utilizamos la extensión 'pg_stat_statements', el sistema va 
acumulando información (cuánto tiempo tardan las consultas, cuántas veces se 
ejecutan, etc.). Este script borra todo ese historial acumulado para poder medir 
el impacto de nuevos cambios (como agregar un nuevo índice o mejorar el código de 
la aplicación) sin que los datos antiguos interfieran.

Archivo SQL: day07_reset_pg_stat_statements.sql

Archivo PNG: day07_reset_pg_stat_statements.png
**********************************************************************************/


-- =====================================================================
-- BLOQUE LÓGICO: Reinicio de métricas
-- =====================================================================

-- Función de PostgreSQL encargada de limpiar las estadísticas acumuladas.
-- Devuelve todos los contadores de rendimiento de las consultas (como tiempos 
-- de ejecución y número de veces que se utilizaron) a su estado inicial de cero.
SELECT pg_stat_statements_reset();
