/*******************************************************************************
Título: Preparación y Enriquecimiento de Datos de Empleados

Objetivo: Crear una tabla de trabajo definitiva y vincularla con catálogos.

Descripción: Este script realiza dos acciones principales:
1. Crea una copia de seguridad/trabajo de los datos maestros de empleados.

2. Añade nuevas columnas para vincular (hacer relaciones) al empleado con
tablas maestras de departamentos, puestos y áreas de estudio, garantizando
la integridad de los datos mediante restricciones (Foreign Keys).
*******************************************************************************/

-- ==============================================================================
-- 1. CREACIÓN DE LA TABLA DE TRABAJO
-- ==============================================================================
-- Se usa DROP si existe para asegurar un estado limpio en lugar de IF NOT EXISTS,
-- lo cual es más seguro si la estructura del origen cambió.
DROP TABLE IF EXISTS employee_final;

-- Se utiliza CTAS (Create Table As Select) que es más rápido que INSERT.
-- Si la tabla es muy grande, añadir 'WITH DATA' o 'NOLOGGING' (en Oracle) 
-- puede acelerarlo, aunque depende del motor.
CREATE TABLE employee_final AS
SELECT *
FROM employee_master_data;-- Copia toda la estructura y datos de la tabla maestra.

-- ==============================================================================
-- 2. ENRIQUECIMIENTO Y RELACIONES (ALTER TABLE)
-- ==============================================================================
-- Modificamos la tabla 'employee_final' para añadir columnas de relación.
ALTER TABLE employee_final
	-- Añade columna para el departamento y lo vincula con el catálogo de departamentos.
	ADD COLUMN department_id INT REFERENCES department_catalog (department_id),
	-- Añade columna para el puesto y lo vincula con el catálogo de roles/puestos.
	ADD COLUMN job_role_id INT REFERENCES job_role_catalog (job_role_id),
	-- Añade columna para el área educativa vinculada al catálogo de estudios.
	ADD COLUMN education_field_id INT REFERENCES education_field_catalog (education_field_id);



/*******************************************************************************
Título: Actualización de llaves foráneas en tabla de empleados

Objetivo: Normalizar la tabla 'employee_final' sustituyendo nombres de texto 
por sus correspondientes IDs (llaves primarias) de tablas de catálogo.

Descripción: El script toma los valores de texto (departamento, puesto, campo de 
estudio) de la tabla 'employee_final', los busca en sus respectivos 
catálogos y actualiza la tabla principal con el ID numérico 
correspondiente para mejorar la integridad referencial.
*******************************************************************************/

-- Actualizar la tabla final de empleados con los IDs correctos de los catálogos
UPDATE employee_final AS e
SET
	-- Asigna el ID del departamento buscando por nombre
	department_id = dc.department_id,
	-- Asigna el ID del puesto de trabajo buscando por nombre
	job_role_id = jrc.job_role_id,
	-- Asigna el ID del campo educativo buscando por nombre
	education_field_id = efc.education_field_id
	-- Define las tablas de catálogo que actúan como fuente de búsqueda
FROM
	department_catalog AS dc, 
	job_role_catalog AS jrc, 
	education_field_catalog AS efc
-- Relaciona las tablas de catálogo con los textos descriptivos de la tabla de empleados
WHERE e.department = dc.department_name-- Coincidencia de departamento
	AND e.job_role = jrc.job_role_name-- Coincidencia de puesto (rol)
	AND e.education_field = efc.education_field_name;-- Coincidencia de campo de estudio



/*******************************************************************************
Título: Limpieza de la tabla final de empleados

Objetivo: Optimizar la estructura de la tabla 'employee_final' eliminando 
columnas de texto redundantes que ya han sido procesadas o mapeadas 
a valores numéricos/categorías, mejorando el rendimiento y reduciendo 
el espacio de almacenamiento.

Descripción: Se eliminan las columnas 'department', 'job_role' y 'education_field' 
debido a que la información ya se encuentra normalizada en otras 
tablas o columnas dentro de la base de datos.
*******************************************************************************/

ALTER TABLE employee_final
-- Elimina la columna 'department' si existe
DROP COLUMN IF EXISTS department,
-- Elimina la columna 'job_role' si existe
DROP COLUMN IF EXISTS job_role,
-- Elimina la columna 'education_field' si existe
DROP COLUMN IF EXISTS education_field;



/* ============================================================
Título: Validación de Estructura de Empleados
   
Objetivo: Verificar la correcta integración de datos.

Descripción: Consulta de muestra para validar que la tabla 
final de empleados esté correctamente vinculada con sus 
catálogos (departamento, puesto, educación), mostrando 
datos clave de rendimiento e ingresos.
============================================================ */

SELECT
	-- Seleccionamos las columnas clave para el reporte
	e.employee_number,         -- ID único del empleado
	dc.department_name,         -- Nombre del departamento (traído del catálogo)
	jrc.job_role_name,          -- Nombre del puesto (traído del catálogo)
	efc.education_field_name,   -- Área de estudio (traída del catálogo)
	e.monthly_income,          -- Ingreso mensual actual
	e.performance_rating-- Calificación de desempeño
FROM
	-- Tabla base: Datos finales de los empleados
	employee_final AS e
-- Unimos con catálogo de departamentos para obtener el nombre
JOIN department_catalog AS dc ON e.department_id = dc.department_id
-- Unimos con catálogo de puestos para obtener el nombre del rol
JOIN job_role_catalog AS jrc ON e.job_role_id = jrc.job_role_id
-- Unimos con catálogo de estudios para obtener el área educativa
JOIN education_field_catalog AS efc ON e.education_field_id = efc.education_field_id
-- Ordenamos por número de empleado para garantizar un orden consistente
ORDER BY
	e.employee_number
-- Limitamos el resultado a las primeras 10 filas para una vista rápida
LIMIT 10;