/*******************************************************************************
 Título: Consulta de Empleados con Ingreso Superior al Promedio
 
Objetivo: Identificar a los empleados que perciben un salario mensual mayor al 
 promedio general de la empresa.

 Descripción: Se calcula primero el sueldo promedio global de la tabla de 
 empleados y, luego, se filtran y ordenan los empleados cuyo ingreso supera esa 
 cifra.

 Archivo SQL: day19_case_study_above_avg_income_qry.sql

 Archivo PNG: day19_case_study_above_avg_income_qry.png
*******************************************************************************/


-- ====================================================================================
-- BLOQUE 1: SELECCIÓN Y ORIGEN DE DATOS
-- Objetivo: Elegir los datos clave de los empleados desde la tabla principal.
-- ====================================================================================
SELECT 
    f.employee_number, -- Número de identificación único de cada empleado
    f.monthly_income    -- Ingreso mensual registrado del empleado
FROM 
    fact_employees AS f -- Tabla principal con los datos laborales

-- ====================================================================================
-- BLOQUE 2: FILTRADO POR PROMEDIO GENERAL
-- Objetivo: Comparar el sueldo de cada persona contra el promedio total.
-- ====================================================================================
WHERE 
    f.monthly_income > ( -- Conserva solo a quienes ganan más que el promedio
        SELECT 
            AVG(monthly_income) -- Calcula el salario promedio de toda la empresa
        FROM 
            fact_employees -- Revisa la lista general de empleados
    )

-- ====================================================================================
-- BLOQUE 3: ORDENAMIENTO DE RESULTADOS
-- Objetivo: Mostrar la lista empezando por quienes ganan más.
-- ====================================================================================
ORDER BY 
    f.monthly_income DESC; -- Ordena de mayor a menor según el ingreso mensual