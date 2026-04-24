/*******************************************************************************
Título: Exportación de Dataset de Empleados en Riesgo
 
Objetivo: Identificar y exportar una lista de empleados con alto sueldo y baja 
satisfacción para análisis de recursos humanos.
 
Descripción: El script selecciona empleados con ingresos superiores a 5000 y 
satisfacción menor a 2, cruzando tablas de departamentos y roles para obtener 
datos legibles. El resultado se guarda en un CSV para análisis posterior en 
Python o Power BI.

Resultado PNG: day02_hr_attrition_risk_factors_exp_data.png
********************************************************************************/

-- Iniciamos el proceso de exportación de datos a un archivo físico
COPY (
    -- Seleccionamos las columnas necesarias para el análisis
    SELECT 
        e.employee_number,    -- Número identificador único del empleado
        dc.department_name,   -- Nombre del departamento (mapeado desde catálogo)
        jrc.job_role_name,    -- Nombre del puesto específico (mapeado desde catálogo)
        e.monthly_income,     -- Ingreso mensual actual para evaluar costo-oportunidad
        e.job_satisfaction,   -- Nivel de satisfacción (1=Bajo, 4=Alto)
        e.attrition           -- Indica si el empleado ya dejó la empresa (Yes/No)
    -- Definimos la tabla principal de empleados
    FROM 
    	employee_final AS e
    -- Unimos con catálogos para obtener nombres legibles en lugar de IDs
    JOIN 
    	department_catalog AS dc 
    	ON e.department_id = dc.department_id
    JOIN 
    	job_role_catalog AS jrc 
    	ON e.job_role_id = jrc.job_role_id
    -- Filtramos para enfocar en: Altos ingresos (>5000) Y baja satisfacción (<2)
    WHERE e.monthly_income > 5000 
      AND e.job_satisfaction < 2
)
-- Definimos la ruta y nombre del archivo de salida
TO 'C:/DM_Lab/DM_Roadmap_P1_120D/02_data/processed/rrhh/employees_attrition.csv'
-- Configuramos el formato del archivo CSV
WITH (
    FORMAT CSV,         -- Formato estándar separado por comas
    DELIMITER ',',      -- Coma como separador de columnas
    HEADER TRUE,        -- Incluye los nombres de las columnas en la primera línea
    ENCODING 'UTF8'     -- Soporte para caracteres especiales (acentos, ñ)
);
