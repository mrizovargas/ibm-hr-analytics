/**********************************************************************************
Título: Limpieza y Homologación de Salarios de Empleados

Objetivo: Garantizar que todos los registros de empleados tengan un salario válido.

Descripción: Este script consulta la información de los empleados desde la tabla de 
datos brutos ("dirty data"). Su función principal es transformar los valores nulos 
(vacíos) en el campo de ingresos mensuales y convertirlos en un valor numérico cero 
(0), evitando así errores en futuros cálculos financieros o reportes.

Archivo SQL: day11_clean_employee_salaries.sql

Archivo CSV: day11_clean_employee_salaries.csv

Archivo PNG: day11_clean_employee_salaries.png
****************************************************************************************/

-- BLOQUE DE SELECCIÓN: Definición de las columnas que queremos consultar.
SELECT 
	-- Identificador único interno del empleado en la base de datos.
	employee_id,
    
	-- Número de nómina o identificación oficial del empleado en la empresa.
	employee_number,
    
	-- Salario original registrado (puede contener espacios vacíos/nulos si no se capturó).
	monthly_income AS salario_mensual_original,
    
	-- Control de vacíos: Si el salario está en blanco (NULL), lo reemplaza con un 0.
	-- Esto asegura que siempre haya un número con el cual operar.
	COALESCE(monthly_income, 0) AS salario_mensual_final

-- BLOQUE DE ORIGEN: Especifica de dónde se extrae la información.
FROM
	-- Tabla origen que contiene los datos en bruto o sin procesar de los empleados.
	employee_master_dirty_data;