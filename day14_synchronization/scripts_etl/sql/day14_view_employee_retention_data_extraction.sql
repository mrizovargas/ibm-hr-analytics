/*****************************************************************************************
 * Título: Creación de Vista del Personal para Análisis de Retención Laboral
 * 
 * Objetivo: Construir una estructura fija (Vista) que almacene los datos limpios y 
 * filtrados de los empleados con estabilidad en la organización.
 * 
 * Descripción: Este script genera o actualiza una vista basada en las variables más 
 * críticas de la tabla maestra de empleados (como salario, departamento, horas extra y 
 * balance de vida). La vista actúa como una ventana directa y siempre actualizada que el 
 * equipo de Recursos Humanos o Analistas de Datos pueden consultar directamente para 
 * evaluar la rotación del personal.
 * 
 * Archivo SQL: day14_view_employee_retention_data_extraction.sql
 * 
 * Archivo CSV: day14_view_attrition_raw.csv
 * 
 * Archivo PNG: day14_view_employee_retention_data_extraction.png
*****************************************************************************************/

-- Le decimos a la base de datos que cree una nueva estructura (Vista) llamada 
-- 'view_employee_retention_data'. Si ya existía una antes con ese nombre, la reemplaza.
CREATE OR REPLACE VIEW view_employee_retention_data AS

	-- Iniciamos la selección de las columnas específicas que formarán parte de nuestra vista
	SELECT
		-- Renombramos los tecnicismos en inglés a un español claro y amigable para el negocio
		employee_id AS id_empleado,
		employee_number AS num_empleado,
		age AS edad,
		department AS departamento,
		job_role AS rol_puesto,
		monthly_income AS ingreso_mensual,
		over_time AS horas_extra,
		work_life_balance AS balance_vida,
		
		-- El campo 'attrition' nos indica de forma directa si el empleado ya causó baja
		attrition AS desgaste
		
	-- Definimos la tabla de origen de donde se extraerá la información original del personal
	FROM
		employee_master_data
		
	-- Establecemos la regla de negocio fundamental para recortar nuestro universo de datos
	WHERE
		-- Solo incluimos a personas que lleven un año o más trabajando de forma activa.
		-- Esto evita sesgar el análisis con empleados nuevos en etapa de inducción.
		years_at_company >= 1;