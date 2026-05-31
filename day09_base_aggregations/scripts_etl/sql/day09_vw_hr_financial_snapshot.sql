/*=================================================================
 Título: Snapshot Financiero y de Recursos Humanos
  
 Objetivo: Crear una vista analítica que consolide y resuma 
 los datos de los empleados por departamento y puesto de trabajo.
  
 Descripción: Esta consulta toma los datos en bruto de la nómina 
 y los agrupa para calcular rápidamente el total de personal, el 
 costo de la nómina y el salario promedio. Facilita la toma de 
 decisiones empresariales de forma eficiente.
 
 Archivo SQL: day09_vw_hr_financial_snapshot.sql
 
 Archivo CSV: day09_vw_hr_financial_snapshot.csv
 
 Archivo PNG: day09_vw_hr_financial_snapshot_01.png
 			  day09_vw_hr_financial_snapshot_02.png
 =================================================================*/

-- Genera o actualiza una vista (consulta guardada) para acelerar y simplificar el análisis de datos
CREATE OR REPLACE VIEW view_hr_financial_snapshot AS 

SELECT 
    department,          -- Agrupa la información por el área o departamento de la empresa
    job_role,            -- Subdivide el grupo anterior según el puesto o cargo específico
    
    COUNT(employee_number) AS total_employees,  -- Cuenta cuántos empleados hay en esa combinación exacta de departamento y puesto
    SUM(monthly_income) AS total_payroll,       -- Suma todos los salarios mensuales para calcular el costo total de esa nómina
    ROUND(AVG(monthly_income), 2) AS average_salary  -- Calcula el salario promedio y lo redondea a exactamente 2 decimales

FROM employee_master_data  -- Extrae toda la información desde la tabla principal de empleados

GROUP BY 
    department,          -- Organiza los cálculos agrupándolos primero por departamento
    job_role;            -- Y luego subdivide esos grupos por puesto de trabajo
