/***************************************************************************************************
Título: CONTROL DE CALIDAD DE DATOS - VALIDACIÓN DE EMPLEADOS SIN PUESTO ASIGNADO

Objetivo: Detectar registros de empleados desalineados en la base de datos de recursos humanos.

Descripción: Este script busca empleados en la tabla de hechos cuyos códigos de puesto están vacíos 
o no existen en el catálogo maestro. Su meta es alertar sobre anomalías antes de armar los reportes, 
evitando que el sistema borre o ignore trabajadores de forma silenciosa al combinar las tablas.

Archivo SQL: day16_validate_unassigned_data.sql

Archivo PNG: day16_validate_unassigned_data.png
****************************************************************************************************/

-- 1. Contamos todas las filas que cumplan con las condiciones de alerta especificadas abajo.
SELECT COUNT(*) AS registros_huerfanos

-- 2. Buscamos directamente en la lista principal que guarda los registros de los empleados.
FROM fact_employees

-- 3. Filtramos bajo dos condiciones: que el puesto esté vacío o que el código no sea válido.
WHERE 
    -- Alerta A: El empleado tiene el campo del puesto totalmente vacío (valor nulo).
    job_id IS NULL 
    
    -- Alerta B: El código del puesto asignado no existe en nuestro catálogo maestro.
    OR job_id NOT IN (
        -- Revisamos la lista oficial de puestos aprobados en la compañía para contrastar.
        SELECT job_id FROM dim_jobs
    );