/*******************************************************************************
TITULO: Creación de Tabla Maestra de Empleados
OBJETIVO: Establecer la estructura base para almacenar la información demográfica,
          organizacional y de compensación de los colaboradores.
DESCRIPCIÓN: Este script crea la tabla 'employee_master_data' si no existe,
             incluyendo campos clave para análisis de retención, movilidad,
             estructura de puestos y compensaciones (sueldos y opciones).
********************************************************************************/

CREATE TABLE IF NOT EXISTS employee_master_data (
    -- =========================================================================
    -- 1. DATOS DEMOGRÁFICOS Y PERSONALES
    -- Información básica del colaborador.
    -- =========================================================================
    age INT NOT NULL,                        -- Edad del colaborador (obligatorio).
    gender VARCHAR(50),                     -- Género registrado.
    marital_status VARCHAR(20),             -- Estado civil (Single, Married, Divorced).
    over18 CHAR(1),                        -- Verificación de mayoría de edad (Y/N).

    -- =========================================================================
    -- 2. INDICADORES DE RETENCIÓN Y MOVILIDAD
    -- Métricas clave para análisis de fuga de talento (Attrition) y traslados.
    -- =========================================================================
    attrition VARCHAR(10),                  -- Abandono de la empresa (Yes/No).
    business_travel VARCHAR(50),            -- Frecuencia de viajes laborales.
    distance_from_home INT,                 -- Distancia al centro de trabajo en km.

    -- =========================================================================
    -- 3. ESTRUCTURA ORGANIZACIONAL Y PUESTO
    -- Ubicación funcional del empleado.
    -- =========================================================================
    department VARCHAR(50),                 -- Área o departamento funcional.
    job_role VARCHAR(50),                   -- Nombre del cargo o función.
    job_level INT,                          -- Nivel de jerarquía en la organización.
    employee_number INT PRIMARY KEY,        -- LLAVE PRIMARIA: Identificador único por colaborador para integridad referencial.
    employee_count INT,                     -- Conteo unitario (usualmente 1 por fila).

    -- =========================================================================
    -- 4. COMPENSACIÓN Y BENEFICIOS
    -- Datos financieros relacionados con el empleo.
    -- =========================================================================
    monthly_income INT,                     -- Sueldo mensual bruto.
    monthly_rate INT,                       -- Tasa o costo mensual relativo.
    daily_rate INT,                         -- Pago por jornada diaria.
    hourly_rate INT,                        -- Pago por hora laborada.
    percent_salary_hike INT,                -- Porcentaje del último incremento.
    stock_option_level INT,                -- Nivel de opciones sobre acciones.

    -- =========================================================================
    -- 5. Educación y Formación
    -- Historial académico y preparación técnica.
    -- =========================================================================
    education INT,                          -- Nivel académico alcanzado (codificado).
    education_field VARCHAR(50),            -- Especialidad o carrera estudiada.
    training_times_last_year INT,           -- Cursos de capacitación tomados el año pasado.

    -- =========================================================================
    -- 6. Encuestas de Satisfacción y Desempeño
    -- Percepción del empleado y calidad de su trabajo (Escalas numéricas).
    -- =========================================================================
    environment_satisfaction INT,           -- Satisfacción con el entorno laboral.
    job_involvement INT,                    -- Nivel de compromiso con el puesto.
    job_satisfaction INT,                   -- Nivel de felicidad en el trabajo.
    performance_rating INT,                 -- Calificación de la última evaluación.
    relationship_satisfaction INT,          -- Calidad de relación con colegas.
    work_life_balance INT,                  -- Equilibrio entre vida y trabajo.

    -- =========================================================================
    -- 7. Trayectoria y Permanencia
    -- Experiencia acumulada dentro y fuera de la organización.
    -- =========================================================================
    num_companies_worked INT,               -- Cantidad de empresas previas.
    total_working_years INT,                -- Años totales de experiencia laboral.
    years_at_company INT,                   -- Antigüedad en la empresa actual.
    years_in_current_role INT,              -- Tiempo en el puesto actual.
    years_since_last_promotion INT,         -- Años desde el último ascenso.
    years_with_curr_manager INT,            -- Tiempo bajo el mando del jefe actual.

    -- =========================================================================
    -- 8. Condiciones Laborales
    -- Parámetros finales sobre la jornada de trabajo.
    -- =========================================================================
    over_time VARCHAR(10),                  -- Realización de horas extra (Yes/No).
    standard_hours INT                      -- Horas base establecidas por contrato.
);