/*******************************************************************************
Título: Auditoría de Salarios en Cero o Negativos

Objetivo: Identificar posibles errores de captura en los ingresos de los empleados.

Descripción: Esta consulta busca registros donde el ingreso mensual es igual o menor 
a cero, lo cual permite detectar datos faltantes o inconsistentes antes de realizar 
análisis financieros.

Archivo SQL: day02_hr_invalid_records_audit.sql

Archivo PNG: day02_hr_invalid_records_audit.png
*********************************************************************************/

-- ---------------------------------------------------------
-- 1. Selección y filtrado de inconsistencias salariales
-- ---------------------------------------------------------

SELECT
    -- Mostramos el número de identificación del empleado para localizarlo fácilmente
	e.employee_number,
    -- Incluimos el departamento para saber a qué área pertenece el registro
	e.department,
    -- Mostramos el ingreso mensual para verificar el valor erróneo
	e.monthly_income
FROM
    -- Consultamos la tabla maestra de empleados y le asignamos el apodo 'e' para abreviar
	employee_master_data AS e
WHERE
    -- Aplicamos el filtro: solo nos interesan los casos con sueldo de 0 o valores negativos
	e.monthly_income <= 0;
	