/***************************************************************************************
 * Título: Clasificación de Riesgo de Desgaste Laboral (Burnout)
 * 
 * Objetivo: Identificar qué empleados podrían estar en riesgo de renunciar o sufrir 
 * desgaste debido a una alta carga de trabajo.
 * 
 * Descripción: Este script analiza los datos del personal combinando las horas extra 
 * trabajadas con su nivel de equilibrio entre vida y trabajo. Con esto, clasifica a los 
 * empleados en tres niveles de riesgo (Alto, Moderado o Estable) para que el equipo de 
 * Recursos Humanos pueda tomar acciones preventivas.
 * 
 * Archivo SQL: day14_employee_burnout_risk_classification.sql
 * 
 * Archivo CSV: day14_employee_burnout_risk_classification.csv
 * 
 * Archivo PNG: day14_employee_burnout_risk_classification.png
 ***************************************************************************************/

-- Iniciamos la selección de los campos que necesitamos mostrar en el reporte final
SELECT 
    -- Cambiamos los nombres técnicos de las columnas a un español claro y amigable
    employee_id AS id_empleado,
    employee_number AS num_empleado,
    over_time AS horas_extra,
    work_life_balance AS equilibrio_vida,
    
    -- Evaluamos la situación de cada empleado para asignarle una categoría de riesgo
    CASE
        -- Si hace horas extra y su equilibrio de vida es bajo (1 o 2), el riesgo es alto
        WHEN over_time = 'Yes' AND work_life_balance IN (1, 2) THEN 'Alto Riesgo'
        
        -- Si hace horas extra pero su equilibrio es mejor (3 o 4), el riesgo es moderado
        WHEN over_time = 'Yes' AND work_life_balance IN (1, 2) THEN 'Riesgo Moderado'
        
        -- Si no cumple con lo anterior (por ejemplo, no hace horas extra), está estable
        ELSE 'Estable'
        
    -- Cerramos la evaluación de condiciones y nombramos esta nueva columna como resultado
    END AS clasificacion_desgaste

-- Indicamos la base de datos o tabla origen donde está guardada la información del personal
FROM
    employee_master_data;