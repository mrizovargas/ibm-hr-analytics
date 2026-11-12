/***********************************************************************************
 Título: Cálculo de la Mediana Salarial de Empleados

 Objetivo: Obtener el punto medio (mediana) de los ingresos mensuales de todos los 
 empleados.

 Descripción: La consulta accede a la tabla de datos de empleados, ordena todos los 
 sueldos de menor a mayor y calcula el valor exacto que se ubica justo a la mitad.

 Archivo SQL: day22_calculate_median_monthly_income.sql

 Archivo PNG: day22_calculate_median_monthly_income.png
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CÁLCULO DE LA MEDIANA DE INGRESOS
-- Objetivo: Ordenar los salarios mensuales y extraer el valor del percentil 50.
-- ====================================================================================

SELECT
    -- Calculamos la mediana (50% de los datos) ordenando primero los ingresos
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_income) AS mediana_ingresos
FROM
    -- Consultamos la tabla principal que almacena los registros de cada empleado
    fact_employees;