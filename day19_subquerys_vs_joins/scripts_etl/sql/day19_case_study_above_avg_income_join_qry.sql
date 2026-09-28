-- Opción B: Enfoque Reescrito a JOIN (Optimizado para proyección de campos)

/*******************************************************************************
 Título: Consulta de Empleados con Ingreso Superior al Promedio con Cruce de 
 Tablas

 Objetivo: Obtener el detalle laboral de los empleados cuyo sueldo supera el 
 promedio global, proyectando puesto, departamento y la media salarial calculada.

 Descripción: Se calcula el promedio general en una subconsulta y se cruza con 
 las tablas de empleados y puestos para filtrar y mostrar solo los sueldos superiores.

 Archivo SQL: day19_case_study_above_avg_income_join_qry.sql

 Archivo PNG: day19_case_study_above_avg_income_join_qry.png
*******************************************************************************/
EXPLAIN ANALYZE

-- ====================================================================================
-- BLOQUE 1: SELECCIÓN DE CAMPOS A MOSTRAR
-- Objetivo: Definir la información final que se presentará en el reporte.
-- ====================================================================================

SELECT 
    f.employee_number,                   -- Identificador único del empleado
    f.monthly_income,                    -- Ingreso mensual del empleado
    j.job_role,                          -- Cargo o puesto de trabajo
    j.department,                        -- Departamento al que pertenece
    ROUND(stats.promedio_gobal, 2) AS promedio_gobal -- Promedio redondeado a 2 decimales

-- ====================================================================================
-- BLOQUE 2: ORIGEN Y COMBINACIÓN DE TABLAS
-- Objetivo: Unir los datos del empleado con su puesto y la media global.
-- ====================================================================================

FROM 
    fact_employees AS f                  -- Tabla con el registro principal de empleados
INNER JOIN 
    dim_jobs AS j                        -- Tabla con el catálogo de puestos y áreas
    ON f.job_id = j.job_id               -- Relación entre el empleado y su puesto de trabajo
CROSS JOIN (
    SELECT 
        AVG(monthly_income) AS promedio_gobal -- Obtiene la media salarial de la empresa
    FROM 
        fact_employees                   -- Consulta la tabla de empleados para la media
) AS stats                                  -- Subconsulta nombrada como tabla temporal de estadísticas

-- ====================================================================================
-- BLOQUE 3: FILTRADO DE DATOS
-- Objetivo: Dejar únicamente a los colaboradores que ganan más que la media.
-- ====================================================================================

WHERE 
    f.monthly_income > stats.promedio_gobal -- Compara el sueldo individual con el promedio general

-- ====================================================================================
-- BLOQUE 4: ORDENAMIENTO DE RESULTADOS
-- Objetivo: Organizar la lista de mayor a menor según el salario percibido.
-- ====================================================================================

ORDER BY 
    f.monthly_income DESC;               -- Ordena de mayor a menor según el ingreso mensual