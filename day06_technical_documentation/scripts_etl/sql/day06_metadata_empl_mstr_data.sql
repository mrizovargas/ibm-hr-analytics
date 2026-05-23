/*******************************************************************************
Título: Consulta de Metadatos de Tabla de Empleados

Objetivo: Obtener el comentario técnico/funcional definido en la base de datos 
para la tabla 'employee_master_data'.

Descripción: Este script consulta el catálogo del sistema PostgreSQL para leer 
la descripción (comentario) asignada a la tabla maestra de empleados en el esquema 
público. Ayuda a entender el propósito de la tabla sin ver los datos.

Archivo SQL: day06_metadata_empl_mstr_data.sql

Archivo PNG: day06_metadata_empl_mstr_data.png
********************************************************************************/

-- Selecciona la descripción de la tabla usando la función nativa de PostgreSQL
SELECT 
    -- Obtiene el comentario de 'public.employee_master_data'
    -- Se castea a 'regclass' para asegurar que encuentre la tabla correctamente
    obj_description('public.employee_master_data'::regclass, 'pg_class') AS comentario_tabla;