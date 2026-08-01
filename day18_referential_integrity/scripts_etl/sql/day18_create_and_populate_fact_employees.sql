/***********************************************************************************
 Título: Creación y población de la tabla de hechos de empleados

 Objetivo: Establecer la tabla principal de empleados relacional e insertar datos 
 iniciales.

 Descripción: El script crea la tabla de hechos 'fact_employees' con una clave 
 foránea conectada a la dimensión de puestos ('dim_jobs'). Posteriormente, inserta 
 tres registros de empleados asignados a sus respectivos puestos e ingresos.

 Archivo SQL: day18_create_and_populate_fact_employees.sql

 Archivo PNG: day18_create_and_populate_fact_employees.png
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CREACIÓN DE LA TABLA Y REGLAS DE INTEGRIDAD
-- Objetivo: Definir la estructura física de empleados y su enlace con los puestos.
-- ====================================================================================

-- Paso 1: Creamos la tabla de empleados si no existe previamente
CREATE TABLE IF NOT EXISTS fact_employees(
	employee_number INT PRIMARY KEY,  -- Identificador único de cada empleado
	age INT,                          -- Edad del empleado expresada en años
	job_id INT,                       -- Clave de asociación hacia la tabla de puestos
	monthly_income DECIMAL(10,2),     -- Sueldo mensual en formato numérico con 2 decimales
	
	-- Paso 2: Definimos la regla de integridad referencial (Clave Foránea)
	CONSTRAINT fk_employees_jobs
		FOREIGN KEY (job_id)                   -- Columna local que sirve como enlace
		REFERENCES dim_jobs(job_id)            -- Columna origen en la tabla catálogo (padre)
		ON UPDATE CASCADE                      -- Actualiza el ID automáticamente si cambia en el padre
		ON DELETE RESTRICT                     -- Evita eliminar un puesto si hay empleados asignados
);


-- ====================================================================================
-- BLOQUE 2: CARGA INICIAL DE REGISTROS DE EMPLEADOS
-- Objetivo: Insertar la información inicial de los colaboradores en la base de datos.
-- ====================================================================================

-- Paso 3: Especificamos la tabla destino y el orden de los campos a llenar
INSERT INTO fact_employees(employee_number, age, job_id, monthly_income)
	VALUES
		(1, 41, 101, 5993.00), -- Empleado 1: 41 años, asociado al puesto 101 ($5,993.00)
		(2, 34, 101, 4500.00), -- Empleado 2: 34 años, asociado al puesto 101 ($4,500.00)
		(3, 28, 102, 3200.00); -- Empleado 3: 28 años, asociado al puesto 102 ($3,200.00)