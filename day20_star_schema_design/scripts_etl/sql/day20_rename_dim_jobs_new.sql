/*******************************************************************************
 Título: Renombrado de Tabla de Dimensión de Puestos (dim_jobs_new a dim_jobs)

 Objetivo: Asignar el nombre definitivo dim_jobs a la nueva estructura de puestos 
 tras la eliminación de la versión legacy.

 Descripción: Renombra la tabla dim_jobs_new para que pase a ser la versión oficial 
 y activa de la dimensión de puestos en la base de datos.

 Archivo SQL: day20_rename_dim_jobs_new.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: RENOMBRADO DE LA ESTRUCTURA PRINCIPAL
-- Objetivo: Establecer el nombre definitivo para la tabla de dimensión de puestos.
-- ====================================================================================

ALTER TABLE dim_jobs_new RENAME TO dim_jobs;                 -- Renombra la tabla de puestos a su nombre oficial