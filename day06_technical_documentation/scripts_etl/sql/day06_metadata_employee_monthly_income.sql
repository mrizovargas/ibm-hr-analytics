/*******************************************************************************
Título: Consulta de Descripción Activa de Columna

Objetivo: 
Obtener la descripción o metadato actual que está configurada en la base de datos 
para un campo específico de una tabla.
 
Descripción: 
Este script consulta el catálogo del sistema para buscar la tabla de empleados y 
extraer el texto que documenta qué significa exactamente el campo de ingresos 
mensuales.

Archivo SQL: day06_metadata_employee_monthly_income.sql

Archivo PNG: day06_metadata_employee_monthly_income.png
 ******************************************************************************/

SELECT 
    -- 1. SELECCIÓN DE LA COLUMNA DE INTERÉS
    -- Seleccionamos el nombre de la columna y la renombramos como 'columna' 
    -- para que el resultado sea más fácil de leer en el reporte final.
    column_name AS columna, 
    
    -- 2. EXTRACCIÓN DE LA DESCRIPCIÓN ACTIVA
    -- Utilizamos una función interna para buscar la documentación oficial o nota
    -- asignada a esta columna específica dentro del esquema de la base de datos.
    col_description(('public.' || table_name)::regclass, ordinal_position) AS descripcion_activa

-- 3. ORIGEN DE LOS DATOS
-- Toda esta información se extrae del catálogo o diccionario oficial de la base 
-- de datos, el cual almacena la estructura de todas las tablas y columnas.
FROM information_schema.columns

-- 4. FILTROS DE BÚSQUEDA
-- Limitamos los resultados para que el sistema busque exclusivamente...
WHERE 
	table_name = 'employee_master_data'  -- ...dentro de esta tabla de empleados.
	AND column_name = 'monthly_income';      -- ...y únicamente sobre el campo de ingresos mensuales.