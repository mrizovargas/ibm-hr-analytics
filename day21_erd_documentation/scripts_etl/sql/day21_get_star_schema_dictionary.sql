/*******************************************************************************
 Título: Auditoría y Extracción de Meta Datos para Documentación ERD 
 (Modelo Estrella)

 Objetivo: Obtener la lista detallada de columnas, tipos de datos y reglas clave 
 (como llaves primarias o foráneas) de las tablas principales del modelo.

 Descripción: Combina las vistas del catálogo 'information_schema' para extraer 
 el diseño de las tablas 'fact_employees', 'dim_jobs' y 'dim_demographics' de la 
 base de datos 'ibm_hr_analytics'.

 Archivo SQL: day21_get_star_schema_dictionary.sql
 
 Archivo MD: day21_get_star_schema_dictionary.md

 Archivo PNG: day21_get_star_schema_dictionary.png
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CONSULTA DE METADATOS Y RESTRICCIONES DE COLUMNAS
-- Objetivo: Identificar la estructura y tipo de regla aplicable a cada campo.
-- ====================================================================================

SELECT 
    t.table_name AS tabla,                  -- Nombre de la tabla consultada
    c.column_name AS columna,                -- Nombre del campo o columna
    c.data_type AS tipo_dato,                -- Tipo de dato (e.g., integer, varchar)
    c.is_nullable AS permite_null,           -- Acepta valores vacíos (YES/NO)
    COALESCE(
        tc.constraint_type, 
        'ATTRIBUTE'
    ) AS tipo_restriccion                    -- Muestra la regla (PK/FK) o 'ATTRIBUTE'
FROM 
    information_schema.tables AS t           -- Vista principal de tablas
JOIN 
    information_schema.columns AS c          -- Relaciona las columnas de cada tabla
    ON t.table_name = c.table_name
    AND t.table_schema = c.table_schema
LEFT JOIN 
    information_schema.key_column_usage AS kcu -- Cruza campos con reglas/llaves
    ON c.table_name = kcu.table_name
    AND c.column_name = kcu.column_name
    AND c.table_schema = kcu.table_schema
LEFT JOIN 
    information_schema.table_constraints AS tc -- Obtiene el tipo de restricción
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.table_schema = tc.table_schema
WHERE 
    t.table_catalog = 'ibm_hr_analytics'      -- Filtra por la base de datos específica
    AND t.table_schema = 'public'             -- Solo en el esquema público
    AND t.table_name IN (                     -- Tablas clave a analizar
        'fact_employees', 
        'dim_jobs', 
        'dim_demographics'
    )
ORDER BY 
    t.table_name,                            -- Ordena por nombre de tabla
    c.ordinal_position;                      -- Mantiene el orden original de campos