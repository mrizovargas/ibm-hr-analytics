/*******************************************************************************
 * Título: Generación de Matriz de Empleados y Puestos
 * 
 * Objetivo: Crear un cruce de datos para obtener todas las combinaciones posibles
 *           entre el personal activo y los roles de trabajo disponibles.
 * 
 * Descripción: El script toma la lista de todos los empleados y la cruza con 
 *              la lista de puestos de trabajo para generar una matriz completa.
 *
 * Archivo SQL: day16_cross_join_active_employees_roles.sql
 ******************************************************************************/

SELECT 
    -- Seleccionamos el número de identificación único de cada empleado
    e.employee_number,
    
    -- Seleccionamos el nombre o título del puesto de trabajo
    d.job_role

-- Indicamos de dónde provienen los datos de los empleados
FROM f at_employees AS e

-- Cruzamos los empleados con los puestos para generar cada combinación
CROSS JOIN dim_jobs AS d; -- Queda claro que buscas una matriz
