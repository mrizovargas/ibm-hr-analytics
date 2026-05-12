/*******************************************************************************
Título: Análisis de Consistencia en Historial de Promociones

Objetivo: Identificar empleados con datos inconsistentes en el sistema.

Descripción: Selecciona empleados cuyo tiempo desde la última promoción es mayor 
que su tiempo total en la empresa, lo que indica un posible error en el registro 
de datos (años de promoción > años en empresa).

Archivo SQL: day04_empl_promo_consistency_audit.sql

Archivo CSV: day04_empl_promo_consistency_audit.csv

Archivo PNG: day04_empl_promo_consistency_audit.png
********************************************************************************/

-- Seleccionamos los datos necesarios para identificar al empleado y revisar sus tiempos
SELECT 
	employee_number,           -- Número único de identificación del empleado
	years_at_company,          -- Años totales que el empleado lleva en la empresa
	years_since_last_promotion -- Años transcurridos desde su última promoción registrada
FROM 
	employee_master_dirty_data       -- Tabla maestra que contiene la información laboral
WHERE 
	-- Filtramos para encontrar solo los registros inconsistentes:
	-- donde la promoción ocurrió antes de que el empleado entrara a la empresa.
	years_since_last_promotion > years_at_company;