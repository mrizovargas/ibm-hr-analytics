/*****************************************************************************
 * Título: Consulta rápida de control de impacto de datos                     
 * 
 * Objetivo: Prevenir la sobrecarga del servidor calculando el tamaño máximo 
 * de la tabla resultante de combinar empleados y departamentos.
 * 
 * Descripción: El script realiza tres cuentas: el total de empleados, el 
 * número de departamentos distintos y la multiplicación de ambos para proyectar 
 * las filas totales de una matriz.
 *
 * ARCHIVO SQL: day16_impact_control_projection.sql
 *
 * Archivo PNG: day16_impact_control_projection.png
 ******************************************************************************/

SELECT 
    -- Cuenta y etiqueta el total exacto de empleados en la tabla principal
    (SELECT COUNT(*) FROM fact_employees) AS filas_izquierda,
    
    -- Cuenta y etiqueta el total de departamentos únicos en la otra tabla
    (SELECT COUNT(DISTINCT department) FROM dim_jobs) AS filas_derecha,
    
    -- Multiplica ambos totales para estimar el tamaño máximo de la consulta
    ((SELECT COUNT(*) FROM fact_employees) * 
     (SELECT COUNT(DISTINCT department) FROM dim_jobs)) AS filas_proyectadas_matriz;
