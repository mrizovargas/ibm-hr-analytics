/*********************************************************************************
 * TÍTULO: Vista Analítica de Personal Activo y Métricas de Permanencia en el Rol
 * 
 * OBJETIVO: Construir una capa analítica limpia para evaluar el rendimiento del 
 * personal.
 * 
 * DESCRIPCIÓN: Este script genera una vista que consolida datos clave de los 
 * empleados para tableros de control de Recursos Humanos (People Analytics). Su 
 * función es triple: filtra únicamente al personal activo, estandariza los 
 * nombres de las columnas al español para los analistas, y calcula dos indicadores
 * críticos de negocio: un indicador binario de horas extras y un índice porcentual 
 * que mide cuánto tiempo ha pasado el empleado en su puesto actual en relación con 
 * toda su vida laboral.
 *
 *Archivo SQL: day13_view_corporate_hr_analytics.sql
 *
 *Archivo PNG: day13_view_corporate_hr_analytics.png
 *********************************************************************************/

-- Crea o actualiza la vista analítica corporativa con los campos seleccionados.
CREATE OR REPLACE VIEW view_corporate_hr_analytics AS 
	SELECT 
		-- Identificadores únicos del empleado para control interno y cruces.
		employee_id AS id_empleado,
		employee_number AS num_empleado,
		
		-- Datos demográficos y de perfil del puesto.
		job_role AS puesto,
		age AS edad,
		attrition AS estatus_baja,
		
		-- Si el sueldo mensual viene vacío (NULL), le asigna un 0 de forma segura.
		COALESCE(monthly_income, 0) AS sueldo_mensual,
		
		-- Transforma el texto ('Yes'/'No') en un indicador numérico rápido (1 o 0).
		CASE
			WHEN over_time = 'Yes' THEN 1
			ELSE 0
		END AS flag_horas_extra,
		
		-- Calcula el porcentaje de vida laboral invertido en el puesto actual.
		-- Evita errores de división entre cero convirtiendo un total de 0 en NULL.
		ROUND(years_in_current_role * 100.0 / NULLIF(total_working_years, 0), 2) 
			AS indice_permanencia_rol
	FROM
		-- Especifica la fuente de datos principal (tabla maestra de empleados).
		employee_master_data
	WHERE
		-- Filtro perimetral de seguridad operativa: solo incluye personal activo.
		attrition = 'No';