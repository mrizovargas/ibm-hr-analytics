/*******************************************************************************
 * Título: Unión de Empleados y Puestos de Trabajo
 *
 * Objetivo: Obtener una lista completa de los puestos de trabajo. Si un empleado 
 * está asignado a un puesto, se incluirán sus datos (número e ingreso mensual).
 *
 * Descripción:
 * 1. Selecciona los datos principales del empleado y del puesto.
 * 2. Toma la tabla de puestos (dim_jobs) como base.
 * 3. Une la información de los empleados (fact_employees) usando el ID del puesto.
 * 4. Al ser un RIGHT JOIN, asegura que todos los puestos aparezcan en la lista.
 *
 * Archivo SQL: day16_right_join_jobs_employees.sql
 *
 * Arcihvo CSV: day16_right_join_jobs_employees.csv
 *
 * Archivo PNG: day16_right_join_jobs_employees.png
 ******************************************************************************/

SELECT 
	-- Número de identificación único asignado a cada empleado en la empresa
	e.employee_number,

	-- Ingreso o salario mensual registrado para ese empleado específico
	e.monthly_income,

	-- Código de identificación del puesto de trabajo (sirve para conectar tablas)
	j.job_id,

	-- Nombre o título oficial del rol o puesto de trabajo
	j.job_role,

	-- Nombre del área o departamento al que pertenece dicho puesto
	j.department

-- Tabla principal que contiene los datos personales y salarios de los empleados
FROM fact_employees AS e

-- Vinculamos la tabla de puestos, asegurando que veamos todos los puestos 
-- sin importar si actualmente tienen a algún empleado asignado en la otra tabla
RIGHT JOIN dim_jobs AS j

-- La conexión se realiza comparando el código de puesto en ambas tablas
ON e.job_id = j.job_id;