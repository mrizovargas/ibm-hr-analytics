/*******************************************************************************
 Título: Creación de Esquema en Estrella para Análisis de Recursos Humanos

 Objetivo: Definir las tablas de dimensiones (puestos y demografía) y la tabla 
 de hechos principal (empleados) utilizando claves sustitutas (IDENTITY) para 
 garantizar la integridad y el rendimiento del modelo.

 Descripción: Crea la infraestructura relacional completa (dim_jobs_new, 
 dim_demographics y fact_employees_new) vinculando métricas de empleados mediante 
 claves foráneas con reglas de actualización en cascada y restricción de borrado.

 Archivo SQL: day20_star_schema_hr_analytics_definition.sql

 Archivo PNG: day20_star_schema_hr_analytics_definition.png
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CREAR DIMENSIÓN DE PUESTOS (dim_jobs_new)
-- Objetivo: Almacenar los roles de trabajo, departamentos y atributos de la posición.
-- ====================================================================================

CREATE TABLE IF NOT EXISTS dim_jobs_new (
    sk_job_id          BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY, -- Clave técnica única
    job_id             BIGINT NOT NULL,                    -- Identificador original de negocio
    job_role           VARCHAR(100) NOT NULL,              -- Título o nombre de la posición
    department         VARCHAR(100) NOT NULL,              -- Área o departamento asignado
    standard_hours     INT NOT NULL,                       -- Horas laborales estándar fijadas
    is_active          BOOLEAN NOT NULL DEFAULT TRUE,      -- Indica si la posición sigue activa
    high_turnover_risk VARCHAR(3),                         -- Indicador de riesgo de rotación
    
    -- Definición de Llave Primaria
    CONSTRAINT dim_jobs_pk PRIMARY KEY (sk_job_id)         -- Clave primaria de la dimensión
);

-- ====================================================================================
-- BLOQUE 2: CREAR DIMENSIÓN DEMOGRÁFICA (dim_demographics)
-- Objetivo: Registrar información personal, perfil educativo y estado civil del personal.
-- ====================================================================================

CREATE TABLE IF NOT EXISTS dim_demographics (
    sk_demographics_id BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY, -- Clave técnica única
    gender             VARCHAR(20) NOT NULL,               -- Género registrado del colaborador
    education_field    VARCHAR(100) NOT NULL,              -- Especialidad o campo de estudio
    marital_status     VARCHAR(20) NOT NULL,               -- Estado civil actual del colaborador
    
    -- Definición de Llave Primaria
    CONSTRAINT dim_demographics_pk PRIMARY KEY (sk_demographics_id) -- Clave primaria
);

-- ====================================================================================
-- BLOQUE 3: CREAR TABLA DE HECHOS CENTRAL (fact_employees)
-- Objetivo: Registrar las métricas cuantitativas principales y sus conexiones relacionales.
-- ====================================================================================

CREATE TABLE IF NOT EXISTS fact_employees_new (
    sk_employee_id     BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY, -- Clave sustituta del hecho
    employee_number    INT NOT NULL,                       -- Número único del empleado
    sk_job_id          BIGINT NOT NULL,                    -- Clave sustituta para enlazar puesto
    sk_demographics_id BIGINT NOT NULL,                    -- Clave sustituta para demografía
    
    -- Métricas de Negocio (Hechos)
    attrition_numeric  INT NOT NULL,                       -- Indicador numérico de salida (0/1)
    attrition          VARCHAR(5) NOT NULL,                -- Estado de rotación registrado
    monthly_income     NUMERIC(10,2) NOT NULL,             -- Sueldo o ingreso mensual
    years_at_company   INT NOT NULL,                       -- Antigüedad en años en la empresa
    total_working_years INT NOT NULL,                      -- Años totales de experiencia laboral
    
    -- Definición de Llave Primaria
    CONSTRAINT fact_employees_pk PRIMARY KEY (sk_employee_id), -- Clave primaria del hecho
    
    -- Definición de Llaves Foráneas
    CONSTRAINT fk_dim_jobs FOREIGN KEY (sk_job_id)         -- Enlace relacional con puestos
        REFERENCES dim_jobs_new(sk_job_id)                 -- Referencia a dimensión de puestos
        ON UPDATE CASCADE                                  -- Actualización en cascada
        ON DELETE RESTRICT,                                -- Previene borrado si hay registros
        
    CONSTRAINT fk_dim_demographics FOREIGN KEY (sk_demographics_id) -- Enlace con demografía
        REFERENCES dim_demographics(sk_demographics_id)    -- Referencia a dimensión demografía
        ON UPDATE CASCADE                                  -- Actualización en cascada
        ON DELETE RESTRICT                                 -- Previene borrado si hay registros
);