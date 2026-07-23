/******************************************************************************************
-- Título: Consulta de Rotación y Datos Laborales de Empleados
-- 
-- Objetivo: Cruzar los ingresos y la rotación del personal con sus departamentos y roles.
-- 
-- Descripción: Este script extrae información clave del personal para entender el panorama 
-- laboral. Conecta la lista histórica de empleados (que tiene datos numéricos como su 
-- sueldo o si dejaron la empresa) con el catálogo de puestos de trabajo. El cruce asegura 
-- que solo veremos en el reporte final a aquellos empleados que tengan un puesto asignado 
-- y válido en el sistema, descartando datos incompletos.
-- 
-- Archivo SQL: day16_employee_attrition_and_job_details.sql
-- 
-- Archivo CSV: day16_employee_attrition_and_job_details.csv
-- 
-- Archivo PNG: day16_employee_attrition_and_job_details.png
 * ******************************************************************************************/

-- PASO 1: Hacemos la lista del súper. Elegimos qué datos específicos queremos ver.
SELECT
	e.employee_number,  -- El número de nómina o credencial con el que identificas al empleado.
	e.attrition,        -- El indicador de "Baja" o "Rotación" (si sigue en la empresa o no).
	e.monthly_income,   -- El sueldo mensual que percibe actualmente el colaborador.
	j.job_role,         -- El título o nombre de su puesto (ej. Analista, Gerente, etc.).
	j.department        -- El departamento al que pertenece (ej. Ventas, RH, Finanzas).

-- PASO 2: Definimos de dónde sale la información principal y cómo se va a conectar.
FROM fact_employees AS e   -- Usamos la tabla de empleados como nuestra base principal ("e").
INNER JOIN dim_jobs AS j   -- Traemos el catálogo de puestos ("j") para pegarlo a los empleados.

-- PASO 3: La regla de oro. Especificamos cómo se van a emparejar las dos tablas.
	ON e.job_id = j.job_id; -- Solo une la información si el código de puesto coincide en ambas.