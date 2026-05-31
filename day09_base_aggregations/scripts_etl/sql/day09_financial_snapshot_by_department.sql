/* ====================================================================
 Título: Consulta de Histórico Financiero de Recursos Humanos
 
 Objetivo: Identificar y analizar las áreas o departamentos que generan 
 el mayor costo operativo para la empresa.
 
 Descripción: Este reporte extrae una fotografía financiera de los datos 
 de RRHH. Ordena la información de mayor a menor costo total de nómina, 
 permitiendo visualizar rápidamente dónde se concentra el mayor gasto en 
 salarios.
 
 Archivo SQL: day09_financial_snapshot_by_department.sql
 
 Archivo CSV: day09_financial_snapshot_by_department.csv
 
 Archivo PNG: day09_financial_snapshot_by_department.png
 ======================================================================*/

-- Extrae (selecciona) todos los datos y registros disponibles de la vista. 
SELECT *

-- Indica que la información se tomará de la vista llamada "view_hr_financial_snapshot"
-- (Una vista es como una consulta guardada que funciona como una tabla lista para usarse).
FROM view_hr_financial_snapshot

-- Ordena los resultados de manera descendente (de mayor a menor) 
-- basándose en la columna del costo total de nómina.
ORDER BY total_payroll DESC;