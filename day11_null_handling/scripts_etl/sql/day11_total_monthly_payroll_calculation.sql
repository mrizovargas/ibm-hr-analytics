/*******************************************************************************
Título: Cálculo del Gasto Total de Salarios Mensuales

Objetivo: Obtener la suma total de los salarios de todos los empleados.

Descripción: Este script realiza una operación de agregación (suma) sobre los 
ingresos mensuales de los empleados de la tabla de datos brutos. Antes de sumar, 
el script aplica una regla de negocio crucial: si algún empleado no tiene un 
salario registrado (valor nulo o vacío), lo convierte temporalmente en cero (0). 
Esto garantiza que la suma final sea exacta y no se rompa por culpa de datos 
faltantes.

Archivo SQL: day11_total_monthly_payroll_calculation.sql

Archivo PNG: day11_total_monthly_payroll_calculation.png
*************************************************************************************/

-- BLOQUE DE SELECCIÓN Y CÁLCULO: Define la operación matemática que queremos realizar.
SELECT 
	-- 1. COALESCE revisa si 'monthly_income' está vacío y, si es así, lo vuelve 0.
	-- 2. SUM toma todos esos salarios (ya corregidos) y los suma en un solo gran total.
	-- 3. AS le da un nombre claro y legible a esa columna de resultado final.
	SUM(COALESCE(monthly_income, 0)) AS total_salario_mensual

-- BLOQUE DE ORIGEN: Especifica la fuente de donde se toman los datos.
FROM
	-- Tabla origen que contiene el histórico o registros brutos de los empleados.
	employee_master_dirty_data;