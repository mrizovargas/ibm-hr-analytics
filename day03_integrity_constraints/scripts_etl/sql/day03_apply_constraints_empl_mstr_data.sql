/*******************************************************************************
Título: Ajuste de Integridad en Datos Maestros de Empleados

Objetivo: Asegurar la calidad y consistencia de los datos en la tabla 
'employee_master_data'.

Descripción: Este script aplica restricciones (constraints) para evitar datos 
nulos en campos clave, validar rangos de edad e ingresos, y garantizar que cada 
empleado tenga un número único.

Archivo SQL: day03_apply_constraints_empl_mstr_data.sql

Archivo PNG: day03_01_apply_constraints_empl_mstr_data.png
			 day03_02_apply_constraints_empl_mstr_data.png
			 day03_03_apply_constraints_empl_mstr_data.png
********************************************************************************/

-- [BLOQUE 1: Definir campos obligatorios]
-- Se asegura que los campos 'employee_number' y 'monthly_income' no queden vacíos
-- para garantizar que todo empleado tenga identificación y salario registrado.
ALTER TABLE employee_master_data
ALTER COLUMN employee_number SET NOT NULL,
ALTER COLUMN monthly_income SET NOT NULL;

-- [BLOQUE 2: Validar reglas de negocio (Rangos)]
-- Se añaden reglas para asegurar que la edad sea coherente (18-100 años)
-- y que el ingreso mensual sea un valor positivo (> 0).
ALTER TABLE employee_master_data
ADD CONSTRAINT chk_age CHECK (age >= 18 AND age <= 100),
ADD CONSTRAINT chk_income CHECK (monthly_income > 0);

-- [BLOQUE 3: Garantizar unicidad]
-- Se añade una restricción para asegurar que no existan dos empleados
-- con el mismo número de identificación (employee_number).
ALTER TABLE employee_master_data
ADD CONSTRAINT unique_employee UNIQUE (employee_number);












