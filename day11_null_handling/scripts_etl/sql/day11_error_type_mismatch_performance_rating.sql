/*******************************************************************************
TÍTULO: Intento de Homologación de Bonos (¡Alerta de Error de Tipado!)

OBJETIVO: Intentar asignar un texto por defecto a los registros sin calificación.

DESCRIPCIÓN: Este script busca transformar los valores nulos en la columna de 
rendimiento ('performance_rating') para que, si un empleado no tiene calificación, 
se muestre el texto 'Sin Bono'. 

⚠️ NOTA CRÍTICA: Este script fallará al ejecutarse. La función COALESCE exige 
 que todos los datos de la lista sean del mismo tipo. Si 'performance_rating' 
 es un número (ej. 1, 2, 3), SQL no te permitirá meter un texto ('Sin Bono') 
 en esa misma columna, provocando un error de conversión de datos.

Archivo SQL: day11_error_type_mismatch_performance_rating.sql

Archivo PNG: day11_error_type_mismatch_performance_rating.png
***********************************************************************************/

-- BLOQUE DE SELECCIÓN CON ERROR DE CONVERSIÓN: Intento de transformación de datos.
SELECT 
	-- 1. COALESCE evalúa la columna 'performance_rating' (que espera números).
	-- 2. Al encontrar un valor nulo, intenta colocar el texto 'Sin Bono'.
	-- 3. ¡Aquí ocurre el fallo! No se puede mezclar texto con números en la misma columna.
	-- 4. AS intentaba renombrar el resultado final como 'bono_limpio'.
	COALESCE(performance_rating, 'Sin Bono') AS bono_limpio

-- BLOQUE DE ORIGEN: Especifica la tabla de donde se extraen los registros.
FROM
	-- Tabla origen con los datos en bruto de los empleados.
	employee_master_dirty_data;