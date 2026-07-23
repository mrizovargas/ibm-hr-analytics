/***************************************************************************************
 * Título: Normalización de Datos y Construcción del Modelo Dimensional (3NF)
 * 
 * Objetivo: Separar la tabla plana original en una dimensión y una tabla de hechos.
 * 
 * Descripción: Este script descompone la estructura redundante original. Primero crea 
 * un catálogo maestro aislado para los puestos de trabajo (dim_jobs) y lo cargo con 
 * valores únicos. Luego, construye la tabla central de empleados (fact_employees) 
 * enlazándola mediante una llave foránea. Esto optimiza el almacenamiento y garantiza 
 * la integridad de los datos.
 *
 *Archivo SQL: day15_normalize_employee_data_to_3nf.sql
 ***************************************************************************************/

-- ---------------------------------------------------------------------------------
-- BLOQUE 1: CREACIÓN DE LA TABLA DE DIMENSIÓN (CATÁLOGO DE PUESTOS)
-- ---------------------------------------------------------------------------------

-- Creamos la tabla que servirá como el único lugar oficial para almacenar los puestos.
CREATE TABLE dim_jobs (
    -- Identificador numérico automático estándar en PostgreSQL.
    job_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Nombre del puesto. No puede estar vacío (NOT NULL) y no se puede repetir (UNIQUE).
    job_role VARCHAR(100) NOT NULL UNIQUE,
    
    -- Área o departamento al que pertenece el puesto. Tampoco acepta valores vacíos.
    department VARCHAR(100) NOT NULL,
    
    -- Cantidad de horas estándar de trabajo asignadas por ley o contrato a este rol.
    standard_hours INT NOT NULL
);


-- ---------------------------------------------------------------------------------
-- BLOQUE 2: POBLADO DE LA DIMENSIÓN CON VALORES ÚNICOS
-- ---------------------------------------------------------------------------------

-- Insertamos los datos directamente en nuestra nueva tabla de catálogo de puestos.
INSERT INTO dim_jobs (job_role, department, standard_hours)

-- Usamos SELECT DISTINCT para ir a la tabla original y extraer los puestos sin repetir.
-- Si el rol 'Sales Executive' aparece 300 veces, aquí solo se tomará una sola vez.
SELECT DISTINCT 
    job_role,
    department,
    standard_hours
FROM employee_master_data;


-- ---------------------------------------------------------------------------------
-- BLOQUE 3: CREACIÓN DE LA TABLA DE HECHOS (REGISTRO DE EMPLEADOS)
-- ---------------------------------------------------------------------------------

-- Creamos la tabla central que guardará las métricas y datos específicos del personal.
CREATE TABLE fact_employees (
    
    -- El número de nómina único del empleado, que funciona como su llave primaria.
    employee_number INT PRIMARY KEY,
    
    -- Código numérico del puesto. Ya no guardamos el texto largo, solo este número de enlace.
    job_id INT,
    
    -- Edad actual del trabajador.
    age INT,
    
    -- Estatus de rotación o baja laboral (indica con un 'Yes' o 'No' si sigue en la empresa).
    attrition VARCHAR(5),
    
    -- Salario mensual o ingresos percibidos por el empleado.
    monthly_income DECIMAL(10,2),
    
    -- Años totales que el empleado lleva trabajando a lo largo de su carrera profesional.
    total_working_years INT,
    
    -- Establecemos un lazo de acero: la columna 'job_id' de esta tabla debe existir 
    -- obligatoriamente dentro de la columna 'job_id' de la tabla de catálogo (dim_jobs).
    FOREIGN KEY (job_id) REFERENCES dim_jobs(job_id)
);


-- ---------------------------------------------------------------------------------
-- BLOQUE 4: MIGRACIÓN Y VINCULACIÓN FINAL DE LOS DATOS DE EMPLEADOS
-- ---------------------------------------------------------------------------------

-- Preparamos la inserción masiva en nuestra tabla de hechos recién estructurada.
INSERT INTO fact_employees (
    employee_number,
    job_id,
    age,
    attrition,
    monthly_income,
    total_working_years
)

-- Seleccionamos la información cruzando las dos tablas en tiempo de ejecución.
SELECT
    e.employee_number,
    j.job_id, -- Nota: Para que este campo traiga datos, 'employee_master_data' 
              -- debe haber sido actualizada previamente con los IDs del catálogo.
    e.age,
    e.attrition,
    e.monthly_income,
    e.total_working_years

-- Partimos de la tabla maestra original a la cual bautizamos temporalmente como 'e'.
FROM employee_master_data e

-- Hacemos una unión interna (INNER JOIN) con nuestro nuevo catálogo 'dim_jobs' (llamado 'j').
-- El motor compara los textos de los puestos ('job_role') y, cuando encuentra la coincidencia
-- perfecta, une el registro del empleado con el identificador numérico correcto.
INNER JOIN dim_jobs j ON e.job_role = j.job_role;