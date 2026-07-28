/*************************************************************************************
 Título: Identificación de Empleados con Sueldo Superior al Promedio Departamental

 Objetivo: Detectar al personal cuyo ingreso mensual supera la media de su área.

 Descripción: Primero calcula el sueldo promedio por cada departamento. Luego, compara 
 el ingreso de cada empleado contra ese promedio y filtra únicamente a quienes ganan
 más que la media de su departamento, presentando la lista ordenada de mayor a menor.

 Archivo SQL: day17_cte_department_high_earners_analysis.sql

 Archivo CSV: day17_cte_department_high_earners_analysis.csv

 Archivo PNG: day17_cte_department_high_earners_analysis.png
*************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CÁLCULO DE PROMEDIOS SALARIALES POR DEPARTAMENTO
-- Objetivo: Obtener el sueldo medio mensual por cada área operacional de la empresa
-- ====================================================================================

WITH avg_department_income AS (
    SELECT
        -- Departamento o área de adscripción del trabajador
        j.department,
        -- Calculamos el salario mensual promedio general del área
        AVG(monthly_income) AS avg_income
    FROM
        -- Tabla de hechos que contiene las métricas y datos salariales
        fact_employees AS f
    JOIN 
        -- Tabla de dimensión que contiene los nombres de puestos y departamentos
        dim_jobs AS j
        ON f.job_id = j.job_id
    GROUP BY 
        -- Agrupamos para calcular una media única por cada área operacional
        j.department
),

-- ====================================================================================
-- BLOQUE 2: FILTRADO DE EMPLEADOS CON INGRESOS DESTACADOS
-- Objetivo: Identificar a los trabajadores que perciben más que la media de su área
-- ====================================================================================

high_earners AS (
    SELECT
        -- Identificador único del colaborador
        f.employee_number,
        -- Sueldo mensual individual percibido actualmente
        f.monthly_income,
        -- Área o departamento donde labora
        j.department,
        -- Rol o puesto de trabajo donde labora
        j.job_role, 
        -- Promedio salarial calculado previamente para su área
        adi.avg_income
    FROM 
        fact_employees AS f
    JOIN 
        dim_jobs AS j
        ON f.job_id = j.job_id
    JOIN 
        -- Unimos con el cálculo de promedios para poder comparar ingresos
        avg_department_income AS adi
        ON j.department = adi.department
    WHERE
        -- Filtramos solo a las personas con sueldo superior al promedio de su departamento
        f.monthly_income > adi.avg_income
)

-- ====================================================================================
-- BLOQUE 3: PRESENTACIÓN Y FORMATO FINAL DE RESULTADOS
-- Objetivo: Dar formato monetario a las cifras y ordenar la lista para análisis
-- ====================================================================================

SELECT 
    -- Número de identificación del empleado
    employee_number,
    -- Departamento al que pertenece
    department,
    -- Rol o puesto de trabajo al que pertenece
    job_role,
    -- Salario mensual individual
    monthly_income,
    -- Convertimos el promedio departamental a numérico y lo redondeamos a dos decimales
    ROUND(avg_income::NUMERIC, 2) AS dept_average
FROM 
    -- Consultamos la lista filtrada de colaboradores destacados
    high_earners
ORDER BY 
    -- Ordenamos los resultados comenzando por los sueldos más altos
    monthly_income DESC;