/*******************************************************************************
 Título: Eliminación de la Tabla de Dimensión Legacy de Puestos (dim_jobs)

 Objetivo: Eliminar del esquema la tabla antigua dim_jobs una vez que la 
 información ha sido migrada exitosamente hacia la nueva estructura.

 Descripción: Ejecuta la eliminación condicional de la tabla de catálogo dim_jobs 
 para liberar espacio y evitar redundancia en la base de datos.

 Archivo SQL: day20_drop_legacy_dim_jobs.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: ELIMINACIÓN DE LA TABLA OBSOLETA
-- Objetivo: Remover la estructura antigua si existe en el sistema.
-- ====================================================================================

DROP TABLE IF EXISTS dim_jobs;                              -- Elimina la tabla de puestos legacy