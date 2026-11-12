/***********************************************************************************
 Título: Detección de Valores Atípicos (Outliers) por Ingresos Mensuales

 Objetivo: Identificar colaboradores con sueldos atípicamente altos utilizando el 
 método estadístico del rango intercuartílico (IQR).

 Descripción: La consulta calcula los cuartiles Q1 y Q3 sobre los ingresos, 
 determina el límite superior estadístico y cruza la información con las tablas de 
 hechos y dimensiones de empleados para filtrar los casos excedentes.

 Archivo SQL: day22_detect_monthly_income_outliers.sql

 Archivo PNG: day22_detect_monthly_income_outliers.png
 
 Archivo CSV: day22_detect_monthly_income_outliers.csv
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CÁLCULO DE CUARTILES Y LÍMITES ESTADÍSTICOS
-- Objetivo: Calcular Q1, Q3, el rango intercuartílico y los límites para detectar outliers.
-- ====================================================================================

-- Definimos una expresión de tabla común (CTE) para calcular los cuartiles salariales
WITH quartiles AS (
    SELECT
        -- Calculamos el primer cuartil (percentil 25) de los ingresos mensuales
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_income) AS q1,
        -- Calculamos el tercer cuartil (percentil 75) de los ingresos mensuales
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_income) AS q3
    FROM
        -- Tabla maestra que contiene la información de los empleados
        fact_employees
),

-- Segunda CTE para calcular el rango intercuartílico (IQR) y los límites de control
limites AS (
    SELECT
        q1,
        q3,
        -- Obtenemos el IQR restando el primer cuartil al tercer cuartil
        (q3 - q1) AS iqr,
        -- Calculamos el límite inferior restando 1.5 veces el IQR a Q1
        q1 - 1.5 * (q3 - q1) AS lower_bound,
        -- Calculamos el límite superior sumando 1.5 veces el IQR a Q3
        q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM
        quartiles
)

-- ====================================================================================
-- BLOQUE 2: FILTRADO Y EXTRACCIÓN DE EMPLEADOS CON INGRESOS ATÍPICOS
-- Objetivo: Consultar los datos de empleados y filtrar aquellos que superan el límite.
-- ====================================================================================

SELECT
    -- Seleccionamos el identificador único del empleado
    f.sk_employee_id,
    -- Seleccionamos el departamento al que pertenece el colaborador
    j.department,
    -- Mostramos el ingreso mensual actual del empleado
    f.monthly_income,
    -- Incluimos el límite superior calculado para referencia de la auditoría
    l.upper_bound
FROM
    -- Tabla principal con los datos maestros de los empleados (alias 'f')
    fact_employees AS f
INNER JOIN
    -- Cruzamos con la dimensión de puestos de trabajo (alias 'j')
    dim_jobs AS j
    -- Relacionamos ambas tablas empleando la llave foránea del puesto
    ON j.sk_job_id = f.sk_job_id
CROSS JOIN
    -- Cruzamos con la tabla calculada de límites estadísticos (alias 'l')
    limites AS l
WHERE
    -- Filtramos únicamente a los empleados cuyo ingreso mensual rebasa el límite superior
    f.monthly_income > l.upper_bound;