/***************************************************************************************
 * Título: Análisis de Riesgo Laboral (Script con Error de Lógica Secuencial)
 * 
 * Objetivo: Identificar empleados en riesgo basándose en sus horas extra y su balance 
 * de vida, evidenciando un error común en la estructura de condiciones.
 * 
 * Descripción: Este script intenta clasificar a los empleados en tres categorías. Sin 
 * embargo, contiene un error crítico: la primera regla del "CASE" es tan amplia que 
 * atrapa a casi todo el personal, provocando que la segunda regla (la que busca el 
 * "Alto Riesgo") quede completamente inutilizada y nunca se ejecute.
 * 
 * Archivoo SQL: day14_example_sql_case_logic_error.sql
 ***************************************************************************************/

-- Iniciamos la selección de datos básicos del personal y su situación laboral
SELECT
    -- Renombramos los campos técnicos a nombres claros y legibles para el negocio
    employee_id AS id_empleado,
    employee_number AS num_empleado,
    over_time AS horas_extra,
    work_life_balance AS equilibrio_vida,
    
    -- ¡ALERTA! Aquí empieza el bloque con el fallo de lógica secuencial
    CASE
        -- ERROR: SQL evalúa de arriba a abajo. Al poner primero que si el balance es
        -- mayor o igual a 2 ya es 'Empleado Satisfecho', el sistema se detiene aquí.
        WHEN work_life_balance >= 2 THEN 'Empleado Satisfecho'
        
        -- ERROR: Esta línea JAMÁS se ejecutará. Si alguien tiene balance 2 y horas extra,
        -- la regla de arriba ya lo atrapó antes, por lo que nadie será 'Alto Riesgo'.
        WHEN over_time = 'Yes' AND work_life_balance = 2 THEN 'Alto Riesgo'
        
        -- Si el empleado tiene un balance menor a 2 (es decir, 1), cae en esta opción
        ELSE 'Otros'
        
    -- Cerramos el embudo de condiciones y guardamos el resultado en esta columna
    END AS calsificacion_erronea

-- Especificamos la tabla origen de donde se extrae la información de los empleados
FROM
    employee_master_data;