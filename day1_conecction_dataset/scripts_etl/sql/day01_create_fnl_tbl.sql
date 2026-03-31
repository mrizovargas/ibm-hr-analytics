/*******************************************************************************
TÍTULO: Preparación y Enriquecimiento de Datos de Empleados
OBJETIVO: Crear una tabla de trabajo definitiva y vincularla con catálogos.
DESCRIPCIÓN:
Este script realiza dos acciones principales:
1. Crea una copia de seguridad/trabajo de los datos maestros de empleados.
2. Añade nuevas columnas para vincular (hacer relaciones) al empleado con
   tablas maestras de departamentos, puestos y áreas de estudio, garantizando
   la integridad de los datos mediante restricciones (Foreign Keys).
*******************************************************************************/

-- ==============================================================================
-- 1. CREACIÓN DE LA TABLA DE TRABAJO
-- ==============================================================================
-- Se crea la tabla 'employee_final' basándose en 'employee_master_data'.
-- 'IF NOT EXISTS' evita errores si el script se ejecuta más de una vez.
CREATE TABLE IF NOT EXISTS employee_final AS 
	SELECT *
	FROM employee_master_data; -- Copia toda la estructura y datos de la tabla maestra.

-- ==============================================================================
-- 2. ENRIQUECIMIENTO Y RELACIONES (ALTER TABLE)
-- ==============================================================================
-- Modificamos la tabla 'employee_final' para añadir columnas de relación.
ALTER TABLE employee_final
    -- Añade columna para el departamento y lo vincula con el catálogo de departamentos.
    ADD COLUMN department_id INT REFERENCES department_catalog(department_id),
    -- Añade columna para el puesto y lo vincula con el catálogo de roles/puestos.
    ADD COLUMN job_role_id INT REFERENCES job_role_catalog(job_role_id),
    -- Añade columna para el área educativa vinculada al catálogo de estudios.
    ADD COLUMN education_field_id INT REFERENCES education_field_catalog(education_field_id);



/*******************************************************************************
TITULO: Actualización de llaves foráneas en tabla de empleados
OBJETIVO: Normalizar la tabla 'employee_final' sustituyendo nombres de texto
          por sus correspondientes IDs (llaves primarias) de tablas de catálogo.
DESCRIPCIÓN: El script toma los valores de texto (departamento, puesto, campo de
             estudio) de la tabla 'employee_final', los busca en sus respectivos
             catálogos y actualiza la tabla principal con el ID numérico
             correspondiente para mejorar la integridad referencial.
*******************************************************************************/

-- Actualizar la tabla final de empleados con los IDs correctos de los catálogos
UPDATE employee_final e
SET 
    -- Asigna el ID del departamento buscando por nombre
    department_id = d.department_id,
    -- Asigna el ID del puesto de trabajo buscando por nombre
    job_role_id = jr.job_role_id,
    -- Asigna el ID del campo educativo buscando por nombre
    education_field_id = ef.education_field_id
-- Define las tablas de catálogo que actúan como fuente de búsqueda
FROM department_catalog d, job_role_catalog jr, education_field_catalog ef
-- Relaciona las tablas de catálogo con los textos descriptivos de la tabla de empleados
WHERE e.department = d.department_name        -- Coincidencia de departamento
  AND e.job_role = jr.job_role_name           -- Coincidencia de puesto (rol)
  AND e.education_field = ef.education_field_name; -- Coincidencia de campo de estudio



/*******************************************************************************
TITULO: Limpieza de la tabla final de empleados
OBJETIVO: Optimizar la estructura de la tabla 'employee_final' eliminando
          columnas de texto redundantes que ya han sido procesadas o mapeadas
          a valores numéricos/categorías, mejorando el rendimiento y reduciendo
          el espacio de almacenamiento.
DESCRIPCION: Se eliminan las columnas 'department', 'job_role' y 'education_field'
             debido a que la información ya se encuentra normalizada en otras
             tablas o columnas dentro de la base de datos.
*******************************************************************************/

-- Eliminamos las columnas de texto originales
-- Esta sentencia modifica la estructura de la tabla 'employee_final' para borrar
-- los campos de texto que ya no son necesarios en el análisis.
ALTER TABLE employee_final
DROP COLUMN department,       -- Elimina la columna con el nombre del departamento
DROP COLUMN job_role,         -- Elimina la columna con el nombre del puesto
DROP COLUMN education_field;  -- Elimina la columna con el área de estudio



/* ============================================================
   TÍTULO: Validación de Estructura de Empleados
   OBJETIVO: Verificar la correcta integración de datos.
   DESCRIPCIÓN: Consulta de muestra para validar que la tabla
   final de empleados esté correctamente vinculada con sus
   catálogos (departamento, puesto, educación), mostrando
   datos clave de rendimiento e ingresos.
   ============================================================ */

-- Seleccionamos las columnas relevantes para la validación:
-- Número de empleado, departamento, puesto, nivel educativo,
-- ingresos mensuales y calificación de desempeño.
SELECT e.employee_number,
       d.department_name,
       jr.job_role_name,
       ef.education_field_name,
       e.monthly_income,
       e.performance_rating
-- Definimos la tabla principal (empleados) como 'e'
FROM employee_final e
-- Unimos con catálogo de departamentos para obtener el nombre
JOIN department_catalog d ON e.department_id = d.department_id
-- Unimos con catálogo de puestos para obtener el nombre del rol
JOIN job_role_catalog jr ON e.job_role_id = jr.job_role_id
-- Unimos con catálogo de estudios para obtener el área educativa
JOIN education_field_catalog ef ON e.education_field_id = ef.education_field_id
-- Limitamos el resultado a 10 registros para una revisión rápida
LIMIT 10;