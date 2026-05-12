/*******************************************************************************
 Título: Inserción de Nuevo Empleado en Maestro de Datos
 
 Objetivo: Registrar un nuevo empleado en la tabla 'employee_master_data' para mantener
 actualizada la información del personal.
 
 Descripción: Este script inserta un solo registro con datos ficticios específicos 
 (número de empleado 9999, departamento de Data Architecture, etc.) en las columnas 
 clave definidas para el control de talento humano.

 Archivo SQL: day01_insert_new_empl_mstr_tbl.sql
 
 Archivo PNG: day01_insert_new_empl_mstr_tbl.png
********************************************************************************/

-- Inicia la inserción de datos en la tabla maestra de empleados
INSERT INTO employee_master_data (
    employee_number, -- ID único del empleado
    age,             -- Edad del empleado
    department,      -- Área funcional
    job_role,        -- Puesto de trabajo
    monthly_income,  -- Salario mensual
    attrition,       -- Indicador de rotación (Sí/No)
    over_18,         -- Validación de mayoría de edad (Y/N)
    standard_hours,  -- Horas laborales estándar
    business_travel  -- Frecuencia de viajes de negocios
)
-- Define los valores específicos para el nuevo registro
VALUES (
    9999,            -- Número de empleado asignado
    99,              -- Edad
    'Data Architecture', -- Departamento
    'Architect',     -- Rol/Puesto
    99999,           -- Ingreso mensual
    'No',            -- No ha presentado rotación
    'Y',             -- Es mayor de 18 años
    80,              -- Horas estándar
    'Non-Travel'     -- Sin viajes de negocios
);