/*******************************************************************************
Título: Script de Creación de Base de Datos para Recursos Humanos

Objetivo: Crear un modelo de datos normalizado para almacenar información de empleados.

Descripción: Este script define catálogos para estandarizar datos (departamentos, roles, educación)
y una tabla central para los datos específicos de cada empleado, asegurando
la integridad referencial.
*******************************************************************************/

-- ==============================================================================
-- BLOQUE 1: Creación de Catálogos (Tablas Maestras)
-- Objetivo: Almacenar valores únicos para evitar duplicidad y estandarizar datos.
-- ==============================================================================

-- Catálogo de Departamentos
CREATE TABLE department_catalog (
	department_id SERIAL PRIMARY KEY,    -- ID único autoincremental
	department_name VARCHAR (50) UNIQUE NOT NULL-- Nombre del departamento (no nulo, único)
);

-- Catálogo de Roles
CREATE TABLE job_role_catalog (
	job_role_id SERIAL PRIMARY KEY,      -- ID único autoincremental
	job_role_name VARCHAR (50) UNIQUE NOT NULL-- Nombre del puesto (no nulo, único)
);

-- Catálogo de Campos Educativos
CREATE TABLE education_field_catalog (
	education_field_id SERIAL PRIMARY KEY, -- ID único autoincremental
	education_field_name VARCHAR (50) UNIQUE NOT NULL-- Área de estudio (no nulo, único)
);



/*******************************************************************************
Título: Migración de Catálogos desde Datos Maestros

Objetivo: Poblar las tablas de catálogo (Departamentos, Roles, Educación) a partir 
de la tabla maestra de empleados, asegurando la unicidad y limpiando valores nulos 
o vacíos.

Descripción: Este script lee la tabla 'employee_master_data' y extrae los valores 
únicos de campos clave para alimentar tablas maestras normalizadas, evitando 
duplicados mediante comprobaciones 'NOT EXISTS'.
********************************************************************************/

-- ==============================================================================
-- Bloque 1: Poblar el catálogo de departamentos
-- ==============================================================================
INSERT INTO department_catalog (department_name)
SELECT DISTINCT e.department-- Selecciona departamentos únicos
FROM employee_master_data AS e
WHERE e.department IS NOT NULL-- Ignora valores nulos
	AND e.department <> ''-- Ignora valores vacíos
	-- Evita intentar insertar lo que ya existe en el catálogo
	AND NOT EXISTS (
		SELECT 1
		FROM department_catalog AS dc
		WHERE dc.department_name = e.department
	);

-- ==============================================================================
-- Bloque 2: Poblar el catálogo de roles laborales (puestos)
-- ==============================================================================
INSERT INTO job_role_catalog (job_role_name)
SELECT DISTINCT e.job_role-- Selecciona puestos de trabajo únicos
FROM employee_master_data AS e
WHERE e.job_role IS NOT NULL-- Ignora valores nulos
	AND e.job_role <> ''-- Ignora valores vacíos
	-- Asegura no duplicar roles ya existentes
	AND NOT EXISTS (
		SELECT 1
		FROM job_role_catalog AS jrc
		WHERE jrc.job_role_name = e.job_role
	);

-- ==============================================================================
-- Bloque 3: Poblar el catálogo de áreas educativas
-- ==============================================================================
INSERT INTO education_field_catalog (education_field_name)
SELECT DISTINCT e.education_field-- Selecciona áreas de estudio únicas
FROM employee_master_data AS e
WHERE e.education_field IS NOT NULL-- Ignora valores nulos
	AND e.education_field <> ''-- Ignora valores vacíos
	-- Asegura no duplicar áreas de estudio ya existentes
	AND NOT EXISTS (
		SELECT 1
		FROM education_field_catalog AS efc
		WHERE efc.education_field_name = e.education_field
	);



/*******************************************************************************
Título: Validación de Catálogos Maestros de RRHH

Objetivo: Verificar la correcta carga de datos en los catálogos fundamentales 
antes de iniciar procesos de importación de empleados o reportes.

Descripción: Este script ejecuta tres consultas independientes para listar y 
ordenar los catálogos de departamentos, roles de trabajo y campos 
educativos, permitiendo al usuario asegurar la integridad de los datos 
referenciales (catálogos).
********************************************************************************/

-- BLOQUE 1: Validación de Departamentos
-- Propósito: Visualizar la lista de departamentos activos para confirmar su existencia y correcta ortografía.
SELECT * 
FROM department_catalog AS dc
ORDER BY dc.epartment_name;-- Ordena alfabéticamente para facilitar la lectura.

-- BLOQUE 2: Validación de Roles de Trabajo
-- Propósito: Revisar el catálogo de puestos/roles para asegurar que las denominaciones sean correctas.
SELECT * 
FROM job_role_catalog AS jrc
ORDER BY jrc.job_role_name;-- Ordena alfabéticamente por nombre del puesto.

-- BLOQUE 3: Validación de Campos Educativos
-- Propósito: Confirmar la lista de áreas de estudio o campos educativos disponibles.
SELECT * 
FROM education_field_catalog AS efc
ORDER BY efc.education_field_name;-- Ordena alfabéticamente por nombre del campo educativo.