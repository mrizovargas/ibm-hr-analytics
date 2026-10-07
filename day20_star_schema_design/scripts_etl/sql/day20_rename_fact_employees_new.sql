/*******************************************************************************
 Título: Renombrado de Tabla de Hechos de Empleados (fact_employees_new a fact_employees)

 Objetivo: Asignar el nombre definitivo fact_employees a la nueva estructura de 
 hechos tras la eliminación de la versión legacy.

 Descripción: Renombra la tabla fact_employees_new para que pase a ser la versión 
 oficial y activa de la tabla central de hechos en el modelo en estrella.

 Archivo SQL: day20_rename_fact_employees_new.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: RENOMBRADO DE LA ESTRUCTURA PRINCIPAL
-- Objetivo: Establecer el nombre definitivo para la tabla central de hechos.
-- ====================================================================================

ALTER TABLE fact_employees_new RENAME TO fact_employees;     -- Renombra la tabla de hechos a su nombre oficial