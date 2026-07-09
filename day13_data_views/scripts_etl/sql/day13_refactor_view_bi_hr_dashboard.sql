/*********************************************************************************
 * Título: Reajuste de Vista de BI por Cambio de Infraestructura (Traducción)
 * 
 * Objetivo: Adaptar la vista intermedia para absorber el cambio de nombre en la 
 * columna de costos sin alterar el reporte final de Power BI.
 * 
 * Descripción: El equipo de TI cambió el nombre de la columna 'daily_rate' por
 * 'costo_diario_operativo' en la tabla principal. Este script reconfigura
 * (mediante OR REPLACE) nuestra vista para que actúe como un traductor. Toma la
 * nueva columna en español y le vuelve a asignar el alias 'daily_rate'. De esta
 * manera, el modelo de datos en Power BI sigue recibiendo los nombres exactamente
 * como los esperaba y el reporte no se rompe.
 *
 *Archivo SQL: day13_refactor_view_bi_hr_dashboard.sql
 *********************************************************************************/

-- Modifica la vista existente (o la crea si no existía) para actualizar su estructura.
CREATE OR REPLACE VIEW view_bi_hr_dashboard AS
	SELECT 
		-- Conserva el ID del empleado sin cambios para mantener las relaciones del modelo.
		employee_number AS employee_number,
		
		-- Sigue extrayendo el departamento para los filtros del dashboard.
		department AS department,
		
		-- ¡El puente de traducción! Lee la nueva columna pero la entrega con el alias original.
		costo_diario_operativo AS daily_rate
	FROM
		-- Consulta directamente la tabla maestra que ya cuenta con la nueva estructura de TI.
		employee_master_data;