/*******************************************************************************
Título: Consulta de Descripción de Columnas - Tabla 'employee_master_data'

Objetivo: Obtener el nombre de cada columna y su descripción (comentario) asociada 
para una tabla específica en PostgreSQL.

Descripción: Este script consulta el diccionario de datos para traer los nombres 
de las columnas y las notas técnicas/funcionales definidas en la  base de datos 
para la tabla 'employee_master_data' en el esquema público.

Archivo SQL: day06_empl_mstr_data_dictionary.sql

Archivo PNG: day06_empl_mstr_data_dictionary.png
**********************************************************************************/

SELECT 
    -- Selecciona el nombre técnico de la columna
    cols.column_name AS columna,
    
    -- Utiliza una función del sistema para obtener el comentario (descripción) 
    -- asociado a la columna en la tabla pg_description
    pg_catalog.col_description(c.oid, cols.ordinal_position::int) AS comentario
FROM 
    -- Tabla estándar que contiene la información de las columnas
    information_schema.columns cols
JOIN 
    -- Une con la tabla interna de PostgreSQL (pg_class) para obtener el ID de la tabla (oid)
    pg_catalog.pg_class c ON c.relname = cols.table_name
WHERE 
    -- Filtro por el nombre de la tabla de interés
    cols.table_name = 'employee_master_data' 
    -- Filtro por el esquema (buenas prácticas para evitar coincidencias en otros esquemas)
    AND cols.table_schema = 'public';