/***********************************************************************************
 Título: Actualización de identificador de puesto de trabajo

 Objetivo: Modificar la clave primaria de un puesto específico en la tabla de 
 dimensión.

 Descripción: El script busca el puesto con identificador 101 en la tabla 'dim_jobs' 
 y actualiza su valor a 501. Debido a la regla ON UPDATE CASCADE definida en las 
 claves foráneas, los registros vinculados en las tablas dependientes se actualizarán 
 de forma automática.

 Archivo SQL: day18_update_job_id.sql

 Archivo PNG: day18_update_job_id.png
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: ACTUALIZACIÓN DE IDENTIFICADOR DE PUESTO
-- Objetivo: Modificar la clave primaria de un puesto específico en el catálogo.
-- ====================================================================================

-- Paso 1: Indicamos la tabla de puestos donde realizaremos la actualización
UPDATE dim_jobs

-- Paso 2: Asignamos el nuevo valor para el identificador del puesto
SET job_id = 501

-- Paso 3: Filtramos para aplicar el cambio únicamente al puesto con ID actual igual a 101
WHERE job_id = 101;