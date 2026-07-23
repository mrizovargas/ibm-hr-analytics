/*******************************************************************************
 * Título: Consulta de Empleados y su Departamento de Ventas
 * 
 * Objetivo: Obtener un listado de empleados junto con el nombre de su 
 * departamento.
 * 
 * Descripción: Este script une la tabla de empleados con la de puestos de 
 * trabajo. Filtra específicamente a los empleados asignados al departamento de 
 * 'Sales'. Gracias al uso de 'LEFT JOIN', si un empleado no pertenece a 'Sales' 
 * o su puesto no es válido, el empleado se conserva en el reporte mostrando un 
 * valor nulo (NULL) en la columna del departamento.
 *
 *Archivo SQL: day16_sales_employees_data_report.sql
 *
 *Archivo PNG: day16_sales_employees_data_report.png
 ******************************************************************************/

-- Aproximación Correcta (Preservación Absoluta)
-- SOLUCIÓN: La condición se procesa en el acoplamiento

SELECT 
    e.employee_number, -- Columna: Número de identificación del empleado
    d.department       -- Columna: Nombre del departamento (ej. 'Sales')
FROM fact_employees AS e -- Tabla principal: Registro histórico de empleados
LEFT JOIN dim_jobs AS d  -- Vinculamos con la tabla de puestos de trabajo
ON e.job_id = d.job_id   -- Relación: Conectamos ambas tablas por el ID del puesto
AND d.department = 'Sales'; -- Condición: Filtramos que el departamento sea 'Sales'

-- Si el puesto no es de 'Sales' o es inválido, el empleado se conserva
-- Esto evita que los empleados sin este puesto desaparezcan del resultado
