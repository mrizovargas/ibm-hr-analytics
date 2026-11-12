/***********************************************************************************
 Título: Auditoría de Consistencia Estadística de Salarios

 Objetivo: Evaluar métricas estadísticas clave de los salarios mensuales para 
 verificar la consistencia y el comportamiento de los datos en la tabla principal.

 Descripción: La consulta procesa la tabla de hechos de empleados para calcular el 
 total de registros, los valores mínimo y máximo de los sueldos, y la desviación 
 estándar redondeada a dos decimales.

 Archivo SQL: day22_statistical_consistency_audit_monthly_income.sql

 Archivo PNG: day22_statistical_consistency_audit_monthly_income.png
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: AUDITORÍA DE CONSISTENCIA ESTADÍSTICA
-- Objetivo: Obtener conteos, extremos y desviación estándar de los salarios mensuales.
-- ====================================================================================

SELECT
    -- Contamos el número total de registros disponibles en la tabla de empleados
    COUNT(*) AS total_registros,
    
    -- Identificamos el sueldo mensual más bajo registrado en el sistema
    MIN(monthly_income) AS min_salario_mes,
    
    -- Identificamos el sueldo mensual más alto registrado en el sistema
    MAX(monthly_income) AS max_salario_mes,
    
    -- Calculamos la desviación estándar de los salarios y redondeamos a dos decimales
    ROUND(CAST(STDDEV(monthly_income) AS NUMERIC), 2) AS desv_std_salario_mes
FROM
    -- Consultamos la tabla principal que almacena los datos de los empleados
    fact_Employees;