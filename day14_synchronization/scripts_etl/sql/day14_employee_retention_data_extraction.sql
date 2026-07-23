/**************************************************************************************
 * Título: Extracción de Datos de Personal para Análisis de Retención
 * 
 * Objetivo: Filtrar y seleccionar la información clave de los empleados que ya tienen 
 * cierta estabilidad en la empresa para evaluar su situación laboral.
 * 
 * Descripción: Este script extrae variables críticas (como sueldo, departamento, edad, 
 * propósito es servir como base limpia de datos para identificar patrones horas extra 
 * y balance de vida) de la tabla de maestros de empleados. Su de desgaste laboral, 
 * enfocándose únicamente en personal con un año o más de antigüedad.
 * 
 * Archivo SQL: day14_employee_retention_data_extraction.sql
 * 
 * Archivo CSV: day14_attrition_raw.csv
 * 
 * Archivo PNG: day14_employee_retention_data_extraction.PNG
**************************************************************************************/

-- Iniciamos la selección de los datos que nos interesa incluir en nuestro reporte final
SELECT 
    -- Traducimos los nombres de las columnas técnicas a un español claro para el negocio
    employee_id AS id_empleado,
    employee_number AS num_empleado,
    age AS edad,
    department AS departamento,
    job_role AS rol_puesto,
    monthly_income AS ingreso_mensual,
    over_time AS horas_extra,
    work_life_balance AS balance_vida,
    
    -- "Attrition" representa si el empleado ha dejado la empresa o sigue activo
    attrition AS desgaste

-- Indicamos la tabla de donde el sistema debe ir a buscar toda esta información
FROM
	employee_master_data

-- Aplicamos una regla de negocio esencial para limpiar y enfocar nuestro análisis
WHERE 
    -- Solo tomamos en cuenta a los empleados que llevan 1 año o más trabajando aquí.
    -- Esto excluye a los recién ingresados que aún están en periodo de adaptación.
	years_at_company >= 1;