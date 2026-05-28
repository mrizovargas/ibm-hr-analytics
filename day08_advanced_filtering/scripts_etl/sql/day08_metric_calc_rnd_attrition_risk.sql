/* =======================================================================================
 * Título: Análisis de Impacto por Riesgo de Fuga de Talento en I&D
 * 
 * Objetivo: Evaluar el costo financiero y el tamaño del riesgo al que se enfrenta 
 * la empresa ante la posible pérdida de personal clave en el área de investigación.
 * 
 * Descripción: Esta consulta identifica a los empleados del departamento de Investigación 
 * y Desarrollo que tienen una alta probabilidad de renunciar y ganan $\$5,000$ o menos al 
 * mes. El sistema calcula dos cosas: cuántos empleados están en esta situación y cuánto 
 * dinero representa mensualmente para la empresa.
 * 
 * Archivo SQL: day08_metric_calc_rnd_attrition_risk.sql
 * 
 * Archivo CSV: day08_metric_calc_rnd_attrition_risk.csv
 * 
 * Archivo PNG: day08_metric_calc_rnd_attrition_risk.png
 * =======================================================================================*/

SELECT 
    -- Bloque de cálculo de métricas clave:
    -- Cuenta cuántos empleados específicos cumplen con nuestras condiciones de riesgo
    COUNT(*) AS total_empleados_riesgo, 
    
    -- Suma los ingresos mensuales de todos estos empleados para obtener el costo total
    SUM(monthly_income) AS impacto_financiero_total 

-- Bloque de selección de datos y filtros:
-- De dónde provienen los datos: tabla principal de información de empleados
FROM employee_master_data 

-- Filtro 1: Nos enfocamos únicamente en el área de Investigación y Desarrollo
WHERE department = "Research & Development" 

-- Filtro 2: Seleccionamos solo a los empleados con alta probabilidad de renunciar
  AND attrition = "Yes" 

-- Filtro 3: Filtramos por un rango salarial, buscando sueldos iguales o menores a $\$5,000$
  AND monthly_income <= 5000;