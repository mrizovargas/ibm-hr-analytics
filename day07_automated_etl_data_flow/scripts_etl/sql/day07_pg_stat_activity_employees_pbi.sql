/*******************************************************************************
Título: Monitoreo de consultas activas en la base de datos
   
Objetivo: Identificar procesos lentos, colgados o en ejecución en la base de datos, 
enfocándose específicamente en los procesos del usuario de PowerBI (pbi_user) o 
en aquellos que buscan información de empleados.
   
Descripción: Esta consulta rastrea la actividad actual del servidor utilizando la 
vista del sistema 'pg_stat_activity'. Ayuda a los administradores a detectar cuánto 
tiempo llevan ejecutándose los reportes o procesos más pesados para garantizar un 
buen rendimiento general del sistema.
   
Archivo SQL: day07_pg_stat_activity_employees_pbi.sql

Archvio PNG: day07_pg_stat_activity_employees_pbi.png   
**********************************************************************************/

SELECT 
    -- [Columna 1] Identificador único del proceso (Process ID o PID)
    -- Permite saber qué número de sesión está ejecutando la acción.
    pid, 
    
    -- [Columna 2] Texto de la consulta SQL que se está ejecutando
    -- Muestra el código exacto que el sistema está procesando en este momento.
    query, 
    
    -- [Columna 3] Estado actual del proceso
    -- Indica si el proceso está 'active' (trabajando), 'idle' (sin hacer nada) 
    -- o en espera de algún recurso.
    state, 
    
    -- [Columna 4] Tiempo de ejecución del proceso
    -- Calcula cuántas horas, minutos o segundos lleva el proceso activo 
    -- desde que inició la consulta hasta el momento exacto de esta revisión.
    age(clock_timestamp(), 
    query_start) AS tiempo_ejecucion

-- [Origen de los datos] Tabla de actividad del sistema
-- Es la 'bitácora' interna de PostgreSQL que guarda todo lo que ocurre 
-- en la base de datos en tiempo real.
FROM pg_stat_activity

-- [Filtros principales] Condiciones de búsqueda
-- Únicamente mostrará resultados si se cumple alguna de estas dos reglas:
WHERE usename = 'pbi_user' 
   OR query LIKE '%employee_master_data%'
