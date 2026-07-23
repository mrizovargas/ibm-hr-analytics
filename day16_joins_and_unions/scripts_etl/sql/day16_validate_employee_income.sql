/***************************************************************************************************
Título: CONTROL DE CALIDAD FINANCIERO - VALIDACIÓN DE INGRESOS ACUMULADOS

Objetivo: Verificar que no se pierda dinero simulado (nómina) al combinar las tablas.

Descripción: Este script calcula y compara la suma total de salarios antes y después de hacer la 
unión de tablas. Si ambos montos finales son idénticos, confirmamos que ningún empleado con salario 
asignado se quedó fuera del reporte final por problemas en sus códigos de puesto.

Archivo SQL: day16_validate_employee_income.sql

Archivo PNG: day16_validate_employee_income_orig.png
			 day16_validate_employee_income_comb.png
*****************************************************************************************************/

-- =================================================================================================
-- BLOQUE 1: CÁLCULO DE LA LÍNEA BASE (Suma original de salarios)
-- =================================================================================================

-- 1. Sumamos todos los salarios mensuales de la tabla para saber el monto real de partida.
SELECT SUM(monthly_income) AS ingresos_originales

-- 2. Extraemos esta información directamente desde la lista maestra de hechos de empleados.
FROM fact_employees;


-- =================================================================================================
-- BLOQUE 2: CÁLCULO DEL REPORTE COMBINADO (Suma de salarios tras el cruce)
-- =================================================================================================

-- 3. Sumamos los salarios de los empleados que pasaron con éxito el filtro de unión de tablas.
SELECT SUM(e.monthly_income) AS ingresos_combinados

-- 4. Volvemos a tomar la lista de empleados, usando la letra 'e' como un atajo para su nombre.
FROM fact_employees AS e

-- 5. Cruzamos la información con el catálogo de puestos (usando el atajo 'd' de dimensión).
INNER JOIN dim_jobs AS d

	-- 6. Condición de cruce: el código del puesto debe coincidir de forma exacta en ambas listas.
    ON e.job_id = d.job_id;