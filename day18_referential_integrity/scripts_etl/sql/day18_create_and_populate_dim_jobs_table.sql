/*******************************************************************************
 Título: Creación, configuración y carga inicial del catálogo de puestos.

 Objetivo: Definir la estructura de la tabla de puestos, asignar su clave 
 primaria e insertar los primeros datos de catálogo.

 Descripción: Crea la tabla 'dim_jobs_qa', le otorga una restricción de unicidad 
 mediante una llave primaria en 'job_id' e inserta un conjunto inicial de puestos.

 Archivo SQL: day18_create_and_populate_dim_jobs_table.sql

 Archivo PNG: day18_create_and_populate_dim_jobs_table_flowchart.png

*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: Estructuración y creación de la tabla
-- Objetivo: Definir las columnas base para almacenar la información de los puestos
-- ====================================================================================

-- Verificamos si la tabla no existe previamente antes de procedera crearla
CREATE TABLE IF NOT EXISTS dim_jobs_qa (
	job_id INT,             -- Identificador único numérico para cada puesto de trabajo
	job_role VARCHAR(100) NOT NULL,   -- Nombre o título del puesto (Obligatorio)
	department VARCHAR(100) NOT NULL -- Área o departamento al que pertenece (Obligatorio)
);

-- ====================================================================================
-- BLOQUE 2: Definición de reglas de integridad
-- Objetivo: Garantizar que no existan IDs duplicados definiendo una clave primaria
-- ====================================================================================

-- Modificamos la tabla creada para establecer que el 'job_id' sea su llave primaria
ALTER TABLE dim_jobs_qa
ADD CONSTRAINT pk_dim_jobs_qa PRIMARY KEY(job_id);

-- ====================================================================================
-- BLOQUE 3: Carga inicial de datos (Poblado del catálogo)
-- Objetivo: Insertar los registros de puestos de trabajo por defecto en la tabla
-- ====================================================================================

-- Agregamos tres registros iniciales asignando su ID, puesto y departamento
INSERT INTO dim_jobs_qa(job_id, job_role, department)
VALUES
	(1, 'Sales Executive', 'Sales'),                         -- Puesto de ventas
	(2, 'Research Scientist', 'Research & Development'),     -- Puesto de investigación
	(3, 'Laboratoty Technician', 'Research & Development');  -- Puesto de laboratorio