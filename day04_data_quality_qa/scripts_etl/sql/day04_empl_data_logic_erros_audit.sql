/*******************************************************************************
Título: Consolidación de Errores en Datos Maestros de Empleados

Objetivo: Identificar inconsistencias lógicas en la tabla 'employee_master_dirty_data'
para depuración de datos.

Descripción: Este script revisa la tabla 'employee_master_dirty_data' para detectar
tres tipos de errores de datos:
   1. Empleados con más años en la empresa que años de experiencia total.
   2. Empleados contratados siendo menores de edad.
   3. Empleados con tiempo desde su último ascenso mayor a su antigüedad.

El resultado muestra el ID, número de empleado y el error encontrado.

Archivo SQL: day04_empl_data_logic_erros_audit.sql

Archivo CSV: day04_empl_data_logic_erros_audit.csv

Archivo PNG: day04_empl_data_logic_erros_audit.png
*********************************************************************************/

-- 1. Bloque: Detectar errores de antigüedad vs experiencia
SELECT 
    employee_id, 
    employee_number, 
    'Error: Antigüedad > Experiencia' AS categoria_error -- Etiqueta el tipo de error encontrado
FROM 
    employee_master_dirty_data 
WHERE 
    years_at_company > total_working_years -- Filtra donde los años en la empresa superan la experiencia total
UNION ALL -- Une los resultados del primer bloque con el siguiente sin eliminar duplicados
-- 2. Bloque: Detectar contratación de menores de edad
SELECT 
    employee_id, 
    employee_number, 
    'Error: Contratación Menor de Edad' -- Etiqueta el tipo de error encontrado
FROM 
    employee_master_dirty_data 
WHERE 
    (age - years_at_company) < 18 -- Calcula la edad de contratación (edad actual - antigüedad) y busca si es menor a 18
UNION ALL -- Une con el siguiente bloque
-- 3. Bloque: Detectar ascensos imposibles
SELECT 
    employee_id, 
    employee_number, 
    'Error: Ascenso Imposible' -- Etiqueta el tipo de error encontrado
FROM 
    employee_master_dirty_data 
WHERE 
    years_since_last_promotion > years_at_company; -- Filtra donde el tiempo desde el ascenso es mayor a la antigüedad total