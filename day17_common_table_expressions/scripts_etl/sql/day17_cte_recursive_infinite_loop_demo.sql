/*************************************************************************************
 Título: Demostración de Bucle Infinito en Consulta Recursiva SQL

 Objetivo: Explicar cómo la ausencia de una condición de parada genera un bucle 
 infinito.

 Descripción: La consulta genera una secuencia numérica partiendo del número 1 y 
 sumando 1 en cada paso. Al no incluir un límite en el paso recursivo, la base de 
 datos intenta generar números indefinidamente hasta agotar recursos o cancelar la 
 tarea.

 Archivo SQL: day17_cte_recursive_infinite_loop_demo.sql

 Archivo PNG: day17_cte_recursive_infinite_loop_demo.png
*************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CONSTRUCCIÓN DE LA SECUENCIA RECURSIVA SIN CONTROL
-- Objetivo: Generar un ciclo numérico iterativo para ilustrar la falta de límite
-- ====================================================================================

WITH RECURSIVE bucle_infinito AS (
    -- MIEMBRO ANCLA: Definimos el punto de partida asignando el valor inicial 1
    SELECT 
        1 AS nivel
		    
    UNION ALL
		    
    -- MIEMBRO RECURSIVO: Tomamos el nivel anterior y le sumamos 1 en cada iteración
    SELECT 
        nivel + 1 
    FROM 
        bucle_infinito
    -- IMPORTANTE: Falta la cláusula WHERE de control (por ejemplo: WHERE nivel < 100)
    -- Sin este filtro, el proceso continúa ejecutándose de manera indefinida
)

-- ====================================================================================
-- BLOQUE 2: CONSULTA Y DESPLIEGUE DE RESULTADOS
-- Objetivo: Intentar mostrar los datos generados por el ciclo recursivo
-- ====================================================================================

SELECT 
    -- Seleccionamos todas las filas generadas durante el proceso de la consulta
    * 
FROM 
    bucle_infinito;