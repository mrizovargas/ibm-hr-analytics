--------------------------------------------------------------------------------
-- TÍTULO: Creación de Catálogo de Departamentos
-- OBJETIVO: Definir la estructura base para almacenar los departamentos de la empresa.
-- DESCRIPCIÓN: Este script crea una tabla maestra (`department_catalog`) que 
--              servirá para categorizar empleados o áreas, garantizando que
--              cada departamento tenga un nombre único y un identificador propio.
--------------------------------------------------------------------------------

-- Bloque de creación de la tabla
CREATE TABLE department_catalog (
	-- Define el ID del departamento como clave primaria, autoincrementable.
	department_id SERIAL PRIMARY KEY,
	-- Define el nombre del departamento: texto hasta 50 caracteres, 
	-- obligatorio (NOT NULL) y sin repetirse (UNIQUE).
	department_name VARCHAR (50) UNIQUE NOT NULL
);



--------------------------------------------------------------------------------
-- TÍTULO: Creación de Catálogo de Roles de Trabajo
-- OBJETIVO: Definir una estructura base para almacenar los diferentes puestos
--          o roles laborales disponibles en la organización.
-- DESCRIPCIÓN: Este script crea la tabla 'job_role_catalog', asegurando que
--              cada rol tenga un identificador único y un nombre no duplicado.
--------------------------------------------------------------------------------

-- Creación de la tabla que funcionará como catálogo maestro de roles
CREATE TABLE job_role_catalog(
	-- Identificador único autoincremental para cada rol (llave primaria)
	job_role_id SERIAL PRIMARY KEY,
	-- Nombre del rol (ej. "Gerente", "Analista"), máximo 50 caracteres,
	-- no permite duplicados y es obligatorio
	job_role_name VARCHAR (50) UNIQUE NOT NULL
);



/*******************************************************************************
 TÍTULO: Creación del Catálogo de Campos Educativos
 
 OBJETIVO:
 Crear una tabla de referencia (catálogo) para almacenar las diferentes áreas,
 disciplinas o campos educativos.
 
DESCRIPCIÓN:
Esta tabla servirá como una tabla maestra para asegurar la integridad referencial
en otras tablas (por ejemplo, en la tabla de empleados o estudiantes), garantizando
que solo se utilicen campos educativos predefinidos.
********************************************************************************/

-- Se crea la tabla 'education_field_catalog' para almacenar el catálogo de campos.
CREATE TABLE education_field_catalog(
	-- Define la clave primaria. 'SERIAL' crea un número entero autoincremental único.
	education_field_id SERIAL PRIMARY KEY,
	-- Define el nombre del campo educativo.
	-- VARCHAR(50): Permite texto de hasta 50 caracteres.
	-- UNIQUE: Asegura que no haya dos campos educativos con el mismo nombre.
	-- NOT NULL: Obliga a que el campo siempre tenga un valor (no permite nulos).
	education_field_name VARCHAR (50) UNIQUE NOT NULL
);



/*******************************************************************************
Título: Poblado de Catálogos Maestros desde Datos de Empleados
Objetivo: Normalizar la base de datos extrayendo valores únicos de departamentos, 
          roles y campos educativos para llenar sus respectivas tablas de catálogo.
Descripción: Este script lee la tabla 'employee_master_data' y toma los valores 
             distintos de las columnas department, job_role y education_field, 
             insertándolos en nuevas tablas de catálogo para evitar duplicidad y 
             mejorar la integridad de los datos.
*******************************************************************************/

-- Bloque 1: Poblar el catálogo de departamentos
-- Extrae nombres de departamentos únicos de la tabla maestra y los inserta en 'department_catalog'.
INSERT INTO department_catalog (department_name)
SELECT DISTINCT department-- Selecciona departamentos distintos
FROM employee_master_data-- Desde la tabla origen
WHERE department IS NOT NULL-- Filtra nulos
AND department <> '';-- Filtra cadenas vacías

-- Bloque 2: Poblar el catálogo de roles laborales (puestos)
-- Extrae los roles únicos de la tabla maestra para alimentar la tabla 'job_role_catalog'.
INSERT INTO job_role_catalog (job_role_name)
SELECT DISTINCT job_role-- Selecciona puestos únicos
FROM employee_master_data-- Desde la tabla origen
WHERE job_role IS NOT NULL-- Filtra nulos
AND job_role <> '';-- Filtra cadenas vacías

-- Bloque 3: Poblar el catálogo de áreas educativas
-- Extrae los campos de estudio únicos de la tabla maestra para la tabla 'education_field_catalog'.
INSERT INTO education_field_catalog(education_field_name)
SELECT DISTINCT education_field-- Selecciona áreas educativas únicas
FROM employee_master_data-- Desde la tabla origen
WHERE education_field IS NOT NULL-- Filtra nulos
AND education_field <> '';-- Filtra cadenas vacías



/*******************************************************************************
TITULO: Validación de Catálogos Maestros de RRHH
OBJETIVO: Verificar la correcta carga de datos en los catálogos fundamentales
          antes de iniciar procesos de importación de empleados o reportes.
DESCRIPCION: Este script ejecuta tres consultas independientes para listar y
             ordenar los catálogos de departamentos, roles de trabajo y campos
             educativos, permitiendo al usuario asegurar la integridad de los datos
             referenciales (catálogos).
********************************************************************************/

-- BLOQUE 1: Validación de Departamentos
-- Propósito: Visualizar la lista de departamentos activos para confirmar su existencia y correcta ortografía.
SELECT * 
FROM department_catalog
ORDER BY department_name;-- Ordena alfabéticamente para facilitar la lectura.

-- BLOQUE 2: Validación de Roles de Trabajo
-- Propósito: Revisar el catálogo de puestos/roles para asegurar que las denominaciones sean correctas.
SELECT * 
FROM job_role_catalog
ORDER BY job_role_name;-- Ordena alfabéticamente por nombre del puesto.

-- BLOQUE 3: Validación de Campos Educativos
-- Propósito: Confirmar la lista de áreas de estudio o campos educativos disponibles.
SELECT * 
FROM education_field_catalog
ORDER BY education_field_name;-- Ordena alfabéticamente por nombre del campo educativo.