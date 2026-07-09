/*********************************************************************************
 * TÍTULO: Conteo de Registro Inicial en Vista de Analítica de Recursos Humanos
 * 
 * OBJETIVO: Determinar el volumen total de registros disponibles en la vista 
 * corporativa.
 * 
 * DESCRIPCIÓN: Este script realiza una consulta directa a la vista unificada de 
 * RH (`view_corporate_hr_analytics`) para contar el número total de filas 
 * (empleados o eventos) cargadas. Sirve como validación inicial para asegurar que 
 * los datos estén completos antes de ejecutar auditorías, análisis de rotación 
 * (Attrition) o reportes.
 * 
 * Archivo SQL: day13_view_corporate_hr_analytics_initial_count.sql
 * 
 * Archivo PNG: day13_view_corporate_hr_analytics_initial_count.png
 *********************************************************************************/

-- 1. Contamos todas las filas de la vista y renombramos la columna para el reporte final.
SELECT 
    COUNT(*) AS total_filas_disponibles
-- 2. Especificamos la fuente de datos (la vista consolidada de analítica de RH).
FROM 
    view_corporate_hr_analytics;