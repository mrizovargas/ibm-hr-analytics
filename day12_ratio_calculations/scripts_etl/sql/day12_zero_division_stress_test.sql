/*******************************************************************************
Título: Simulación de Métricas para Roles Emergentes (Prueba de Estrés)

Objetivo: Validar el comportamiento del cálculo de promedios con datos ficticios 
o vacíos.

Descripción: El script crea un puesto de trabajo "fantasma" (sin empleados ni 
ingresos reales) para demostrar cómo las funciones de agregación y las reglas de 
división reaccionan y se protegen contra errores de división por cero.

Archivo SQL: day12_zero_division_stress_test.sql

Archivo CSV: day12_zero_division_stress_test.csv

Archivo PNG: day12_zero_division_stress_test.png
*********************************************************************************/

-- 1. SELECCIÓN Y PROCESAMIENTO DE DATOS (Bloque Principal)
-- Aquí se reciben los datos de la subconsulta y se calcula el promedio final.
SELECT
	roles.rol_emergente, -- Muestra el nombre del puesto que creamos abajo ("Data Auditor").
	
	-- CÁLCULO DEL PROMEDIO PROTEGIDO Y REDONDEADO:
	-- SUM(...) intenta sumar los ingresos (que son 0).
	-- COUNT(...) cuenta los IDs de empleados (que es NULL, por lo que el conteo da 0).
	-- NULLIF(..., 0) transforma ese conteo de '0' en un 'NULL' para evitar que el sistema se rompa al dividir.
	-- ROUND(..., 2) toma el resultado final y lo limita a 2 decimales.
	ROUND(SUM(roles.ingreso_simulado) / NULLIF(COUNT(roles.empleado_id), 0), 2) AS promedio_seguro

-- 2. ORIGEN DE LOS DATOS (Subconsulta en memoria)
-- Como no estamos usando una tabla física de la base de datos, inventamos un escenario temporal.
FROM (
	-- Este bloque simula una fila de datos con un rol nuevo que aún nadie ocupa.
	SELECT
		'Data Auditor (Emergente)' AS rol_emergente, -- Nombre inventado para el puesto.
		NULL::INT AS empleado_id,                -- Representa que hay 0 empleados (vacío).
		0 AS ingreso_simulado                        -- Representa que no hay dinero asignado aún.
	) AS roles -- Le damos el apodo "roles" a este bloque de datos inventados.

-- 3. AGRUPACIÓN LÓGICA
-- Agrupa el resultado por el nombre del puesto para que las funciones matemáticas (SUM y COUNT)
-- procesen correctamente la información de ese rol específico.
GROUP BY 
	roles.rol_emergente;