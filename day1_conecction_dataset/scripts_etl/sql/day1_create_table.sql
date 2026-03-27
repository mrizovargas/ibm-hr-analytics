/* 
================================================================================
TÍTULO: CREACIÓN DE ESTRUCTURA PARA DATOS BRUTOS (RAW DATA)
================================================================================

OBJETIVO: 
Definir la tabla inicial "employee_master_data" para la ingesta masiva de información 
de Recursos Humanos.

DESCRIPCIÓN DEL OBJETIVO: 
Esta tabla funciona como una "zona de aterrizaje" (Staging Area). Su finalidad 
es recibir los datos del archivo origen (CSV) sin procesar, manteniendo todas 
las métricas originales (desde salarios hasta niveles de satisfacción) para 
luego realizar la limpieza y normalización necesaria.
*/

CREATE TABLE IF NOT EXISTS employee_master_data (
    -- Datos Demográficos y Personales
    age INT NOT NULL,                        -- Edad del colaborador (obligatorio).
    gender VARCHAR(50),                     -- Género registrado.
    marital_status VARCHAR(20),             -- Estado civil (Single, Married, Divorced).
    over18 CHAR(1),                        -- Verificación de mayoría de edad (Y/N).

    -- Indicadores de Retención y Movilidad
    attrition VARCHAR(10),                  -- Abandono de la empresa (Yes/No).
    business_travel VARCHAR(50),            -- Frecuencia de viajes laborales.
    distance_from_home INT,                 -- Distancia al centro de trabajo en km.

    -- Estructura Organizacional y Puesto
    department VARCHAR(50),                 -- Área o departamento funcional.
    job_role VARCHAR(50),                   -- Nombre del cargo o función.
    job_level INT,                          -- Nivel de jerarquía en la organización.
    employee_number INT PRIMARY KEY,        -- Identificador único (Llave Primaria).
    employee_count INT,                     -- Conteo unitario (usualmente 1 por fila).

    -- Compensación y Beneficios
    monthly_income INT,                     -- Sueldo mensual bruto.
    monthly_rate INT,                       -- Tasa o costo mensual relativo.
    daily_rate INT,                         -- Pago por jornada diaria.
    hourly_rate INT,                        -- Pago por hora laborada.
    percent_salary_hike INT,                -- Porcentaje del último incremento.
    stock_option_level INT,                -- Nivel de opciones sobre acciones.

    -- Educación y Formación
    education INT,                          -- Nivel académico alcanzado (codificado).
    education_field VARCHAR(50),            -- Especialidad o carrera estudiada.
    training_times_last_year INT,           -- Cursos de capacitación tomados el año pasado.

    -- Encuestas de Satisfacción y Desempeño (Escalas numéricas)
    environment_satisfaction INT,           -- Satisfacción con el entorno laboral.
    job_involvement INT,                    -- Nivel de compromiso con el puesto.
    job_satisfaction INT,                   -- Nivel de felicidad en el trabajo.
    performance_rating INT,                 -- Calificación de la última evaluación.
    relationship_satisfaction INT,          -- Calidad de relación con colegas.
    work_life_balance INT,                  -- Equilibrio entre vida y trabajo.

    -- Trayectoria y Permanencia
    num_companies_worked INT,               -- Cantidad de empresas previas.
    total_working_years INT,                -- Años totales de experiencia laboral.
    years_at_company INT,                   -- Antigüedad en la empresa actual.
    years_in_current_role INT,              -- Tiempo en el puesto actual.
    years_since_last_promotion INT,         -- Años desde el último ascenso.
    years_with_curr_manager INT,            -- Tiempo bajo el mando del jefe actual.

    -- Condiciones Laborales
    over_time VARCHAR(10),                  -- Realización de horas extra (Yes/No).
    standard_hours INT                      -- Horas base establecidas por contrato.
);