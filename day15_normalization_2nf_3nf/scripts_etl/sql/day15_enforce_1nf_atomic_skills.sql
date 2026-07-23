/************************************************************************************
 * Título: Corrección de Atomicidad mediante Separación de Valores (1NF)
 *
 * Objetivo: Transformar datos no atómicos multivalorados en registros individuales.
 * 
 * Descripción: Este script soluciona una violación a la Primera Forma Normal (1NF) 
 * donde un campo almacena una lista de elementos separados por comas. Mediante una 
 * función de parseo de texto, dividimos esa lista para que cada habilidad quede en 
 * su propia fila independiente, logrando estructuras limpias aptas para búsquedas e 
 * indexación eficiente.
 *
 * Archivo SQL: day15_enforce_1nf_atomic_skills.sql
 ************************************************************************************/

-- Iniciamos la proyección extrayendo el ID del empleado y su habilidad desarmada
SELECT 
    employee_number, -- Mantenemos el número de empleado para saber a quién pertenece el dato.
    value AS skill  -- Renombramos la columna temporal 'value' generada por la función
                    -- a un nombre de negocio mucho más descriptivo como lo es 'skill'.

-- Especificamos la tabla origen que contiene el campo con los datos concatenados
FROM employee_master_data

-- Aplicamos un operador de cruce dinámico (CROSS APPLY) junto con la función del motor.
-- STRING_SPLIT toma la celda 'employee_skills', busca cada coma (',') que pusimos como
-- separador y desarma el texto largo en múltiples filas individuales en tiempo real.
CROSS APPLY STRING_SPLIT(employee_skills, ',');