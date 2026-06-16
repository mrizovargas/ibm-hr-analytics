/*******************************************************************************
Título: Análisis de Ingresos por Departamento y Rol Laboral

Objetivo: Calcular el impacto financiero de la nómina y los promedios salariales.

Descripción: El script agrupa a los empleados por su área y puesto para obtener 
el gasto total en sueldos, el conteo de personal y un promedio salarial seguro 
(evitando errores matemáticos si no hay datos).

Archivo SQL: day12_income_analysis_by_role.sql

Archivo CSV: day12_income_analysis_by_role.csv

Archivo PNG: day12_income_analysis_by_role.png
*********************************************************************************/

-- 1. SELECCIÓN Y PROCESAMIENTO DE DATOS
-- En este bloque definimos qué columnas queremos ver y calculamos las métricas clave.
SELECT 
	department AS departamento, -- Trae el departamento y lo renombra para el reporte.
	job_role AS rol_trabajo,     -- Trae el puesto o rol y lo renombra para claridad.
	
	-- SUMA TOTAL: Suma los ingresos mensuales de todos los empleados del mismo grupo.
	ROUND(SUM(monthly_income),2) AS ingreso_total, 
	
	-- CONTEO: Cuenta cuántos empleados pertenecen a cada puesto y departamento.
	COUNT(*) AS total_empleados,
	
	-- PROMEDIO PROTEGIDO: Divide el ingreso total entre el número de empleados.
	-- Usamos NULLIF para que, si el conteo es 0, el sistema no falle por "división por cero".
	ROUND(SUM(monthly_income) / NULLIF(COUNT(*), 0),2) AS ingreso_promedio_protegido

-- 2. ORIGEN DE LOS DATOS
-- Indicamos la tabla maestra de donde se extraerá toda la información del personal.
FROM
	employee_master_data

-- 3. AGRUPACIÓN LÓGICA
-- Como usamos funciones de suma y conteo, agrupamos los resultados para que se muestren
-- organizados por cada combinación única de Departamento y Rol de trabajo.
GROUP BY
	department,
	job_role

-- 4. ORDENAMIENTO FINAL
-- Organiza el reporte alfabéticamente por "departamento" y, dentro de cada departamento,
-- muestra primero a los roles con mayor "ingreso promedio" (de mayor a menor).
ORDER BY
	departamento,
	ingreso_promedio_protegido DESC;