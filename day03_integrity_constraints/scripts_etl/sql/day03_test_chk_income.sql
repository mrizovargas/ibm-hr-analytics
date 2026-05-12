/*******************************************************************************
 Título: Prueba de Integridad de Datos - Sueldos Negativos
 
 Objetivo: Validar que la restricción (CHECK constraint) 'chk_income' funcione 
 correctamente al intentar insertar datos inválidos.
 
 Descripción: Este script intenta insertar un registro de empleado con un sueldo 
 negativo ($ -1000$). Se espera que la base de datos rechace esta operación 
 debido a una regla de negocio que prohíbe ingresos menores a cero.
 
 Archivo SQL: day03_test_chk_income.sql
 
 Archivo PNG: day03_test_chk_income.png
********************************************************************************/

-- Intenta insertar un registro de prueba con un sueldo negativo
INSERT INTO employee_master_data (
    employee_number,  -- Identificador único del empleado
    age,              -- Edad del empleado
    department,       -- Área o departamento
    monthly_income    -- Sueldo mensual (aquí ocurre la validación)
)
VALUES (
    8889,             -- Número de empleado ficticio
    30,               -- Edad ficticia
    'Test_Dept',      -- Departamento de prueba
    -1000             -- Valor negativo diseñado para disparar el chk_income
);