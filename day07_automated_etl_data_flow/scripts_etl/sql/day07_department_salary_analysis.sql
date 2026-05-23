/*******************************************************************************
Título: Análisis de Personal y Salarios por Departamento

Objetivo: Obtener métricas clave de los empleados según su área de trabajo.

Descripción: El script agrupa los registros del personal para contar el total 
de trabajadores y calcular el sueldo promedio por cada departamento.

Archivo SQL: day07_department_salary_analysis.sql

Archivo CSV: day07_department_salary_analysis.csv

Archivo PNG: day07_department_salary_analysis.png
********************************************************************************/

-- BLOQUE DE EXTRACCIÓN Y CÁLCULO
-- Selecciona el departamento y calcula el total de personas junto con su sueldo promedio.
SELECT 
    department, -- Identifica el departamento actual.
    COUNT(*) AS total_empleados, -- Cuenta cuántos empleados hay en este departamento.
    ROUND(AVG(monthly_income), 2) AS salario_promedio -- Calcula el ingreso mensual promedio y lo redondea a dos decimales.

-- BLOQUE DE ORIGEN DE DATOS
-- Define la tabla principal donde se encuentra archivada la información del personal.
FROM 
    employee_master_data

-- BLOQUE DE AGRUPACIÓN
-- Organiza todos los resultados anteriores agrupándolos por cada departamento encontrado.
GROUP BY 
    department;

