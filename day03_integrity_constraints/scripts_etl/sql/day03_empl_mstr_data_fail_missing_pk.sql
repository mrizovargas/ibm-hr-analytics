/*******************************************************************************
Título: Inserción Fallida - Validación de Nulos

Objetivo: Demostrar el error de integridad al omitir una columna obligatoria.

Descripción: Se intenta insertar un nuevo registro en la tabla maestra de 
empleados omitiendo intencionalmente el campo 'employee_number' (número de empleado), 
lo que debe provocar un error de restricción (NOT NULL) en la base de datos.

Resultado Esperado: Error indicando que la columna "employee_number" no puede ser nula.

Archivo SQL: day03_empl_mstr_data_fail_missing_pk.sql

Archivo PNG: day03_empl_mstr_data_fail_missing_pk.png
*********************************************************************************/

-- Intentamos insertar un empleado omitiendo el número de empleado (clave primaria/obligatoria)
INSERT INTO employee_master_data (
    employee_number,    -- Columna omitida deliberadamente
    age,                -- Edad del empleado
    department,         -- Departamento al que pertenece
    monthly_income      -- Ingreso mensual
)
VALUES (
    30,                 -- Valor para 'age'
    'Test_Dept',        -- Valor para 'department'
    5000                -- Valor para 'monthly_income'
);