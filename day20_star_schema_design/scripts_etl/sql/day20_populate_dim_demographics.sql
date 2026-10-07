/*******************************************************************************
 Título: Vaciado y Poblado Oficial de la Dimensión Demográfica (dim_demographics)

 Objetivo: Reiniciar la tabla de dimensión demográfica y repoblarla con 
 combinaciones únicas de atributos de empleados procedentes de la fuente maestra.

 Descripción: Limpia completamente la tabla dim_demographics reseteando sus 
 contadores e inserta los valores distintos de género, área de estudio y estado 
 civil extraídos desde employee_master_data.

 Archivo SQL: day20_populate_dim_demographics.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: REINICIO Y VACIADO DE LA TABLA DESTINO
-- Objetivo: Vaciar la dimensión y reiniciar el contador de claves autonuméricas.
-- ====================================================================================

TRUNCATE TABLE dim_demographics RESTART IDENTITY CASCADE;    -- Vacía la tabla y reinicia los IDs

-- ====================================================================================
-- BLOQUE 2: DEFINICIÓN DE ESTRUCTURA Y COLUMNAS DE DESTINO
-- Objetivo: Especificar la tabla y campos receptores para el registro demográfico.
-- ====================================================================================

INSERT INTO dim_demographics (
    gender,                  -- Género o identidad registrada del colaborador
    education_field,         -- Campo o área de formación académica
    marital_status           -- Estado civil actual del empleado
)

-- ====================================================================================
-- BLOQUE 3: SELECCIÓN Y EXTRACCIÓN DE PERFILES ÚNICOS
-- Objetivo: Obtener combinaciones de atributos sin duplicados desde la fuente maestra.
-- ====================================================================================

SELECT DISTINCT 
    gender,                  -- Extrae los valores únicos de género
    education_field,         -- Extrae los campos de estudio sin repetir
    marital_status           -- Extrae las variantes registradas de estado civil
FROM 
    employee_master_data;    -- Tabla maestra origen de datos de empleados