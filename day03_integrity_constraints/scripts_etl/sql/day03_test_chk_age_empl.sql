/*******************************************************************************
 Título: Prueba de Restricción de Edad en Empleados
 
 Objetivo: Validar que la base de datos impida el registro de empleados menores 
 de edad.
 
 Descripción: Este script intenta insertar un registro con una edad inválida (15 años)
 para verificar que el check constraint 'chk_age' funcione correctamente y rechace 
 la operación.
 
 Archivo SQL: day03_test_chk_age_empl.sql
 
 Archivo PNG: day03_test_chk_age_empl.png
*******************************************************************************/

-- (Prueba de Edad): Intenta insertar un empleado menor de edad para disparar el chk_age
-- Inserción de prueba: Se intentan cargar datos de un empleado de 15 años
INSERT INTO employee_master_data (
    employee_number, -- ID único del empleado
    age,             -- Campo a validar (menor de edad)
    department,      -- Área de asignación
    monthly_income   -- Sueldo mensual
)
VALUES (
    8888,            -- Número de empleado ficticio para la prueba
    15,              -- Edad que debe disparar el error del chk_age
    'Test_Dept',     -- Departamento de prueba
    5000             -- Salario de prueba
);











