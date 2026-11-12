/***********************************************************************************
 Título: Perfilamiento Estadístico y Análisis de Distribución de Sueldos

 Objetivo: Calcular métricas descriptivas clave sobre los ingresos mensuales de los 
 empleados para entender el comportamiento general de la compensación.

 Descripción: La consulta procesa la tabla de hechos de empleados para extraer el 
 total de registros, el conteo de valores válidos, el sueldo promedio, la mediana, 
 así como los valores mínimo y máximo de los ingresos mensuales.

 Archivo SQL: day22_statistical_profiling_monthly_income.sql

 Archivo PNG: day22_statistical_profiling_monthly_income.png
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: PERFILAMIENTO ESTADÍSTICO DE INGRESOS MENSUALES
-- Objetivo: Obtener métricas agregadas como conteo, promedio, mediana, mínimo y máximo.
-- ====================================================================================

SELECT
    -- Contamos el número total de filas o registros disponibles en la tabla
    COUNT(*) AS total_registros,

    -- Contamos únicamente los registros que tienen un valor asignado en el sueldo
    COUNT(monthly_income) AS non_null_sueldo_mes,

    -- Calculamos el valor promedio o media aritmética de los ingresos mensuales
    AVG(monthly_income) AS avg_sueldo_mes,

    -- Calculamos la mediana (percentil 50) ordenando los sueldos de menor a mayor
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_income) AS mediana_sueldo_mes,

    -- Identificamos el sueldo mensual más bajo registrado en la empresa
    MIN(monthly_income) AS min_sueldo_mes,

    -- Identificamos el sueldo mensual más alto registrado en la empresa
    MAX(monthly_income) AS max_sueldo_mes
FROM
    -- Consultamos la tabla principal que almacena los registros de los empleados
    fact_employees;