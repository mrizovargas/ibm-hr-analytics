/*******************************************************************************
Título: Vista de Segmentación de Riesgo de Retención de Talento

Objetivo: Identificar y clasificar el nivel de riesgo de rotación de los empleados.

Descripción: Esta vista consolida datos clave de los colaboradores y evalúa su 
nivel de estabilidad laboral ("Crítico", "Medio" o "Estable") cruzando variables 
de satisfacción, antigüedad y horas extra.

Archivo SQL: day10_vw_talent_risk_segmentation.sql

Archivo PNG: day10_vw_talent_risk_segmentation.png
**********************************************************************************/

-- Crea o actualiza la vista en la base de datos
CREATE OR REPLACE VIEW view_talent_risk_satisfaction AS
SELECT
    -- Bloque 1: Datos de identificación del empleado
	employee_id,             -- Identificador único del sistema
	employee_number,         -- Número de nómina o registro interno
    
    -- Bloque 2: Información del puesto actual
	department,              -- Área o departamento donde trabaja
	job_role,                -- Puesto o rol que desempeña
	years_in_current_role,   -- Años que lleva en su puesto actual
    
    -- Bloque 3: Indicadores de bienestar laboral
	over_time,               -- Indica si el empleado trabaja horas extra (Yes/No)
	job_satisfaction,        -- Nivel de satisfacción en el trabajo (escala numérica)
	
    -- Bloque 4: Reglas de negocio para calcular el segmento de riesgo
	CASE
        -- Alerta Máxima: Trabaja horas extra, está insatisfecho (<=2) y lleva un año o menos en el rol
		WHEN over_time = 'Yes' AND job_satisfaction <= 2 AND years_in_current_role <= 1 THEN 'Crítico'
        
        -- Alerta Media: Hace horas extra o tiene una satisfacción moderada (=3)
		WHEN over_time = 'Yes' OR job_satisfaction = 3 THEN 'Medio'
        
        -- Situación Ideal: No cumple los criterios anteriores y se considera en bajo riesgo
		ELSE 'Estable'
	END AS risk_segment     -- Etiqueta final del nivel de riesgo del empleado

-- Origen de los datos
FROM
	employee_master_data;   -- Tabla principal con el historial del personal

	