/*********************************************************************************
 * Título: Vista de Conexión para Dashboard de Power BI (Métricas de Nómina)
 * 
 * Objetivo: Crear una capa intermedia segura y optimizada para alimentar el 
 * reporte de BI.
 * 
 * Descripción: Este script expone únicamente las columnas esenciales de la tabla
 * maestra de empleados (`employee_number`, `department` y `daily_rate`)
 * necesarias para los tableros visuales en Power BI. El uso de esta vista actúa
 * como un puente de desacoplamiento: si la estructura de la base de datos
 * subyacente cambia en el futuro, solo se debe ajustar esta vista sin romper el
 * origen de datos del modelo analítico o dashboard final.
 * 
 * Archivo SQL: day13_view_bi_hr_dashboard.sql
 *********************************************************************************/

-- Si la vista de conexión ya existía, la actualiza con los campos más recientes.
CREATE OR REPLACE VIEW view_bi_hr_dashboard AS
	SELECT
		-- Mantiene el identificador único de cada empleado para cruces de datos.
		employee_number AS employee_number,
		
		-- Extrae el departamento para segmentar y filtrar los reportes en BI.
		department AS department,
		
		-- Tarifa diaria; este alias específico es el que mapea el modelo de Power BI.
		daily_rate AS daily_rate
	FROM
		-- Tabla maestra de origen que centraliza el historial del personal.
		employee_master_data;