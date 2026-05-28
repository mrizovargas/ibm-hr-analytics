/* ==============================================================================
 * Título: Análisis de Rotación de Empleados de Investigación y Desarrollo
 * 
 * Objetivo: Identificar perfiles de alto riesgo de fuga en áreas clave.
 * 
 * Descripción: El script localiza empleados del departamento de Investigación y 
 * Desarrollo que ganan menos de $\$5,000$ y han decidido renunciar. 
 * 
 * Archivo SQL: day08_attrition_risk_analysis.sql
 * 
 * Archivo CSV: day08_attrition_risk_analysis.csv
 * 
 * Archivo PNG: day08_attrition_risk_analysis_01.png
 * 				day08_attrition_risk_analysis_02.png
 * ==============================================================================*/

/* ====================================
 * BLOQUE 1: ------ OPTIMIZACIÓN ------
 * ====================================*/
-- Este bloque crea un índice para acelerar la búsqueda. En lugar de revisar toda la 
-- base de datos, crea una lista organizada internamente basada en el departamento, 
-- la rotación y el salario.
CREATE INDEX idx_employee_perf_attrition 
ON employee_master_data(department, attrition, monthly_income);

/* ==================================
 * BLOQUE 2: ------ EXTRACCIÓN ------
 * ==================================*/
-- Este bloque realiza la consulta final para obtener la información detallada de los 
-- empleados.
SELECT 
    employee_id,      -- Identificador único interno del empleado.
    employee_number,  -- Número de identificación visible o de nómina del empleado.
    age,              -- Edad actual del empleado.
    department,       -- Área o departamento al que pertenece (ej. Investigación y 
    				  -- Desarrollo).
    job_role,         -- Puesto o cargo que desempeña.
    monthly_income    -- Ingreso mensual percibido por el empleado.
FROM 
    employee_master_data -- Tabla principal de donde se extrae toda la información del 
    					 -- personal.
WHERE 
    department = 'Research & Development' -- Filtra los resultados para incluir únicamente 
    									  -- al personal de Investigación y Desarrollo.
    AND attrition = 'Yes'                 -- Filtra para incluir solo a los empleados que 
    									  -- han renunciado.
    AND monthly_income <= 5000;           -- Filtra para mostrar solo a quienes ganan $5,000 
    									  -- o menos al mes.
