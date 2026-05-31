/*******************************************************************************
Título: Análisis de Masa Salarial y Antigüedad por Departamento

Objetivo: Obtener métricas clave de capital humano por cada área de la empresa.

Descripción: El script agrupa al personal por su departamento actual para calcular 
la inversión total en sueldos (masa salarial) y el tiempo promedio que los 
empleados llevan trabajando en la compañía.

Archivo: SQL: day09_salary_cost_by_department.sql

Archivo CSV: day09_salary_cost_by_department.csv

Archivo: PNG: day09_salary_cost_by_department.png
*********************************************************************************/

-- BLOQUE DE SELECCIÓN Y CÁLCULO
-- Especifica los datos que queremos mostrar en el reporte final.
SELECT 
	-- Identifica el departamento del empleado.
    department,
    -- Suma los sueldos mensuales para obtener el gasto total por área.
    SUM(monthly_income) AS masa_salarial_total,
    -- Calcula los años promedio de lealtad del equipo en la empresa.
    ROUND(AVG(years_at_company),2) AS promedio_antigüedad

-- ORIGEN DE LOS DATOS
-- Define la base de datos principal de donde se extrae la información.
FROM 
	-- Tabla maestra que contiene el historial de los empleados.
    employee_master_data

-- BLOQUE DE AGRUPACIÓN
-- Consolida los datos individuales en subtotales por cada área.
GROUP BY 
	-- Junta las filas para que los cálculos (SUM y AVG) se apliquen por departamento.
    department;
