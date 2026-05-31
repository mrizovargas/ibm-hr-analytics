/* ==============================================================================
 TÍTULO: Resumen de Ingresos y Cantidad de Empleados

 OBJETIVO: Obtener el total de ingresos mensuales y el conteo de todos los empleados.

 DESCRIPCIÓN: Este bloque calcula dos métricas clave a partir de la base de datos de 
 empleados: 
             1. La suma de todos los ingresos mensuales de la nómina.
             2. El número total de empleados registrados. 

 Archivo SQL: day09_employee_financial_overview.sql
 
 Archivo CSV: day09_employee_financial_overview.csv
 
 Archivo PNG: day09_employee_financial_overview.png
=================================================================================*/

SELECT 
    -- SUM() suma todos los valores de la columna; aquí calcula el total de los ingresos mensuales de todos los empleados
    SUM(monthly_income) AS v1,
    
    -- COUNT() cuenta el número de filas; aquí cuenta cuántos registros únicos de empleados existen
    COUNT(employee_number) AS c1

FROM 
    -- Define la tabla de origen de donde se extraerán y calcularán los datos mencionados
    employee_master_data;
