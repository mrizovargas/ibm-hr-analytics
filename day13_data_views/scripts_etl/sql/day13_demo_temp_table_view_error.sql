/*********************************************************************************
 * Título: Análisis de Empleados Activos y Demostración de Error de Persistencia
 * 
 * Objetivo: Filtrar personal activo en una tabla temporal y exponer un error 
 * común al intentar vincularla a una vista permanente.
 * 
 * Descripción: Este script tiene fines educativos y de control de calidad (QA).
 * Primero, aisla a los empleados sin bajas en una tabla temporal de acceso
 * rápido. Segundo, expone un "antipatrón" o error crítico: intentar crear una
 * vista global que dependa de una tabla efímera. Esto sirve para documentar por
 * qué el sistema fallará en cuanto el analista cierre su sesión o consola de base
 * de datos.
 *
 *Archivo SQL: day13_demo_temp_table_view_error.sql
 *********************************************************************************/

-- ===============================================================================
-- 1. CREACIÓN DE LA TABLA TEMPORAL
-- ===============================================================================

-- Crea una tabla intermedia que solo existirá mientras la sesión actual esté abierta.
CREATE TEMPORARY TABLE temp_empleados_activos AS
	SELECT 
		*
	FROM 
		employee_master_data
	WHERE 
		-- Filtra para conservar únicamente al personal que sigue activo.
		attrition = 'No';


-- ===============================================================================
-- 2. ¡ERROR CRÍTICO! (DEMOSTRACIÓN DE ANTIPATRÓN DE DISEÑO)
-- ===============================================================================

-- Intenta crear una estructura permanente (VIEW) apuntando a datos volátiles.
CREATE VIEW view_empleados_seguros AS
	SELECT 
		*
	FROM 
		-- ¡Peligro! Si esta tabla temporal desaparece, la vista quedará rota e inútil.
		temp_empleados_activos;