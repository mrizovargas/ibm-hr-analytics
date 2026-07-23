/**************************************************************************************
 Título: Análisis del Plan de Ejecución para Uniones (INNER JOIN)

 Objetivo: Inspeccionar la estrategia que utiliza PostgreSQL para combinar tablas.

 Descripción: Este script utiliza la sentencia EXPLAIN para mostrar el plan de
 ejecución generado por el motor de base de datos al unir empleados y puestos.

 Archivo SQL: day16_explain_employee_job_join.sql
 
 Archivo PNG: day16_explain_employee_job_join_1.png
 			  day16_explain_employee_job_join_2.png
*****************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CONFIGURACIÓN DE SESIÓN (DESACTIVACIÓN DE SCAN SECUENCIAL)
-- Objetivo: Obligar a PostgreSQL a evitar la lectura completa de la tabla.
-- ====================================================================================

-- Le indicamos al motor que no use escaneos secuenciales (lectura fila por fila)
-- durante esta sesión, forzándolo a preferir el uso de índices existentes.
SET enable_seqscan = off;

-- ====================================================================================
-- BLOQUE 2: DIAGNÓSTICO DEL PLAN DE EJECUCIÓN (EXPLAIN)
-- Objetivo: Solicitar al motor que muestre cómo procesará la consulta internamente.
-- ====================================================================================

-- Le pedimos a PostgreSQL que ejecute la consulta e imprima un reporte detallado 
-- del tiempo real empleado, el costo y la estrategia utilizada para buscar los datos.
EXPLAIN ANALYZE

-- ====================================================================================
-- BLOQUE 3: SELECCIÓN Y UNIÓN DE TABLAS
-- Objetivo: Definir los datos a extraer y cómo se relacionan entre ambas tablas.
-- ====================================================================================

SELECT
    e.employee_number, -- Número identificador único asignado a cada uno de los empleados.
    j.job_role,        -- Nombre o título descriptivo del rol que desempeña el empleado.
    j.department       -- Área o departamento funcional al que pertenece dicho puesto.

FROM fact_employees AS e -- Tomamos la tabla principal de empleados (con alias 'e').

-- Unimos la tabla de empleados con el catálogo de puestos de trabajo (alias 'j').
INNER JOIN dim_jobs AS j
    -- Definimos que la unión se realice donde coincida el identificador del puesto.
    ON e.job_id = j.job_id

-- ====================================================================================
-- BLOQUE 4: FILTRADO DE RESULTADOS
-- Objetivo: Restringir la búsqueda a un puesto para evaluar el uso del índice.
-- ====================================================================================

-- Filtramos únicamente los empleados asignados al puesto número 5. Esto fuerza
-- al motor a usar el índice en 'job_id' en lugar de recorrer toda la tabla, lo
-- cual ocurre típicamente en tablas pequeñas (ej. 3,000 registros).
WHERE e.job_id = 5;

-- ====================================================================================
-- BLOQUE 5: RESTAURACIÓN DE LA CONFIGURACIÓN DE SESIÓN
-- Objetivo: Reactivar el comportamiento estándar del planificador de PostgreSQL.
-- ====================================================================================

-- Volvemos a habilitar la opción de lectura secuencial para que las siguientes
-- consultas de la sesión elijan su estrategia de búsqueda de forma automática.
SET enable_seqscan = on;