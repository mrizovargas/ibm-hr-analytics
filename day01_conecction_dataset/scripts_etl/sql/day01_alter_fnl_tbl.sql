/*******************************************************************************
TÍTULO: Actualización de llaves foráneas en tabla de empleados
OBJETIVO: Normalizar la tabla 'employee_final' reemplazando nombres descriptivos
          por sus respectivos IDs (llaves primarias) de tablas de catálogo.
DESCRIPCIÓN: Este script transforma las columnas de texto (Departamento, Puesto,
             Área de estudio) en la tabla 'employee_final' en IDs numéricos
             haciendo búsquedas en las tablas maestras (catálogos).
********************************************************************************/

-- Se utiliza ALTER TABLE para modificar la estructura y datos de la tabla employee_final
ALTER TABLE employee_final AS
	SELECT
		-- Seleccionamos los IDs de los catálogos en lugar de los nombres originales
		d.department_id,    -- ID encontrado en la tabla de departamentos
		jr.job_role_id,     -- ID encontrado en la tabla de puestos
		ef.education_field_id -- ID encontrado en la tabla de áreas de estudio
	FROM employee_final e
	-- Buscamos el ID del departamento comparando el nombre actual con el catálogo
	LEFT JOIN department_catalog d ON e.department = d.department_name
	-- Buscamos el ID del puesto de trabajo comparando el nombre actual con el catálogo
	LEFT JOIN job_role_catalog jr ON e.job_role = jr.job_role_name
    -- Buscamos el ID del área de estudio comparando el nombre actual con el catálogo
	LEFT JOIN education_field_catalog ef ON e.education_field = ef.education_field_name;
