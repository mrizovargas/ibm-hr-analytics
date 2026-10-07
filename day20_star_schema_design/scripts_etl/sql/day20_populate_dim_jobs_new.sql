/*******************************************************************************
 Título: Carga de Datos a la Nueva Dimensión de Puestos (dim_jobs_new)

 Objetivo: Poblar la nueva tabla de dimensión de puestos transfiriendo los 
 registros existentes desde la tabla de origen dim_jobs.

 Descripción: Copia los campos de catálogo de puestos (identificador, rol, área, 
 horas, estado e indicador de riesgo) hacia la nueva estructura relacional.

 Archivo SQL: day20_populate_dim_jobs_new.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: DEFINICIÓN DE DESTINO PARA LA INSERCIÓN DE DATOS
-- Objetivo: Especificar la tabla y columnas receptoras en la nueva dimensión.
-- ====================================================================================

INSERT INTO dim_jobs_new (
    job_id,             -- Código único de negocio del puesto
    job_role,           -- Nombre o título de la posición laboral
    department,         -- Departamento o área de trabajo
    standard_hours,     -- Horas laborales estándar establecidas
    is_active,          -- Estado de actividad de la plaza
    high_turnover_risk  -- Indicador de riesgo alto de rotación
)

-- ====================================================================================
-- BLOQUE 2: SELECCIÓN Y ORIGEN DE DATOS
-- Objetivo: Extraer la información existente desde el catálogo previo.
-- ====================================================================================

SELECT 
    job_id,             -- Toma el código de negocio original
    job_role,           -- Toma la descripción de la posición
    department,         -- Toma la categoría o departamento
    standard_hours,     -- Toma la jornada laboral registrada
    is_active,          -- Toma la condición actual de la plaza
    high_turnover_risk  -- Toma el nivel de riesgo asignado
FROM 
    dim_jobs;           -- Tabla origen que contiene los datos a migrar