/*******************************************************************************
 Título: Análisis Salarial y Conteo de Personal por Departamento y Puesto

 Objetivo: Calcular la plantilla total y el salario promedio mensual para cada 
 puesto de trabajo dentro de sus respectivos departamentos.

 Descripción: Consulta la tabla de hechos cruzándola con la dimensión de puestos 
 para agrupar a los empleados, calcular promedios salariales redondeados a dos 
 decimales y ordenar los resultados de menor a mayor sueldo.

 Archivo SQL: day20_salary_analysis_by_job.sql

 Archivo PNG: day20_salary_analysis_by_job.png
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CONSULTA ANALÍTICA Y AGRUPACIÓN DE SALARIOS
-- Objetivo: Obtener métricas de personal y salarios agrupadas por departamento y puesto.
-- ====================================================================================

SELECT 
    j.department,            -- Nombre del departamento al que pertenece el puesto
    j.job_role,              -- Título o rol específico del trabajo
    COUNT(f.sk_employee_id) AS total_empleados, -- Cantidad total de colaboradores
    ROUND(AVG(f.monthly_income), 2) AS salario_promedio -- Sueldo promedio con 2 decimales
FROM 
    fact_employees AS f      -- Tabla de hechos con métricas de empleados
JOIN 
    dim_jobs AS j ON f.sk_job_id = j.sk_job_id -- Une catálogo de puestos por llave
GROUP BY 
    j.department,            -- Agrupa los resultados por departamento
    j.job_role               -- Agrupa los resultados por título del puesto
ORDER BY 
    salario_promedio DESC;    -- Ordena de mayor a menor según el salario promedio