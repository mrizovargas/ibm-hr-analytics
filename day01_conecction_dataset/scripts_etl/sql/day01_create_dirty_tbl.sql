/*******************************************************************************
  Título: Creación de Tabla Maestra de Empleados (Datos Sucios)
  
  Objetivo: 
  Crear una tabla denominada 'employee_master_dirty_data' para almacenar 
  información cruda (sin limpiar) del personal.
  
  Descripción:
  Esta tabla sirve como repositorio inicial para importar datos de recursos humanos.
  Se define 'employee_number' como la clave primaria (única) y se incluyen
  datos demográficos, laborales y de desempeño con los tipos de datos adecuados.
  Se utiliza 'IF NOT EXISTS' para evitar errores si la tabla ya fue creada previamente.
********************************************************************************/

-- Creamos la tabla solo si no existe para evitar errores de duplicidad
CREATE TABLE IF NOT EXISTS employee_master_dirty_data (
    -- =========================================================================
    -- 1. DATOS DEMOGRÁFICOS Y PERSONALES
    -- Información básica para conocer el perfil del colaborador.
    -- =========================================================================
    employee_id VARCHAR(10) NOT NULL,          -- ID único alfanumérico
    age INT NOT NULL,                          -- Edad (campo obligatorio)
    country VARCHAR(20),                       -- País
    city VARCHAR(20),                          -- Ciudad
    gender VARCHAR(50),              -- Género con el que se identifica.
    marital_status VARCHAR(20),      -- Estado civil (Soltero, Casado, Divorciado).
    over_18 VARCHAR(5),              -- Confirmación legal de mayoría de edad (Y/N).
    
    -- =========================================================================
    -- 2. INDICADORES DE RETENCIÓN Y MOVILIDAD
    -- Datos para medir el riesgo de que el talento se vaya de la empresa.
    -- =========================================================================
    attrition VARCHAR(10),           -- Indica si el empleado dejó la empresa (Yes/No).
    business_travel VARCHAR(50),     -- Qué tanto viaja por motivos de trabajo.
    distance_from_home INT,          -- Distancia de su casa a la oficina en km.
    
    -- =========================================================================
    -- 3. ESTRUCTURA ORGANIZACIONAL Y PUESTO
    -- Define dónde encaja el empleado dentro de la jerarquía de la compañía.
    -- =========================================================================
    department VARCHAR(50),          -- Área funcional (Ventas, IT, RRHH, etc.).
    hire_date DATE,                  -- Fecha de ingreso
    job_role VARCHAR(50),            -- Nombre específico de su cargo.
    job_level INT,                   -- Nivel de responsabilidad (del 1 al 5).
    employee_number INT PRIMARY KEY, -- Identificador único (DNI/ID) que no se repite.
    employee_count INT,              -- Auxiliar para conteos estadísticos (siempre es 1).
    
    -- =========================================================================
    -- 4. COMPENSACIÓN Y BENEFICIOS
    -- Todo lo relacionado con pagos y retribución económica.
    -- =========================================================================
    monthly_income INT,              -- Salario mensual fijo.
    monthly_rate INT,                -- Costo total mensual para la empresa.
    daily_rate INT,                  -- Cuánto percibe por día laborado.
    hourly_rate INT,                 -- Pago desglosado por hora.
    percent_salary_hike INT,         -- Porcentaje de aumento en su último incremento.
    stock_option_level INT,          -- Nivel de acceso a acciones de la empresa.

    -- =========================================================================
    -- 5. EDUCACIÓN Y FORMACIÓN
    -- Preparación académica y capacitación continua.
    -- =========================================================================
    education INT,                   -- Nivel de estudios (del 1 al 5).
    education_field VARCHAR(50),     -- Carrera o área de especialidad.
    training_times_last_year INT,    -- Cuántos cursos tomó el año pasado.

    -- =========================================================================
    -- 6. ENCUESTAS DE SATISFACCIÓN Y DESEMPEÑO
    -- Cómo se siente el empleado y qué tan bien hace su trabajo.
    -- =========================================================================
    environment_satisfaction INT,    -- Qué tanto le gusta su espacio físico de trabajo.
    job_involvement INT,             -- Nivel de compromiso con sus tareas.
    job_satisfaction INT,            -- Qué tan feliz se siente en su puesto.
    performance_rating INT,          -- Nota de su última evaluación de desempeño.
    relationship_satisfaction INT,   -- Qué tal se lleva con sus compañeros.
    work_life_balance INT,           -- Equilibrio entre vida personal y laboral.

    -- =========================================================================
    -- 7. TRAYECTORIA Y PERMANENCIA
    -- Historial de tiempo y experiencia acumulada.
    -- =========================================================================
    num_companies_worked INT,        -- En cuántas empresas trabajó antes de esta.
    total_working_years INT,         -- Años totales de experiencia profesional.
    years_at_company INT,            -- Cuánto tiempo lleva en esta empresa.
    years_in_current_role INT,       -- Cuánto tiempo lleva haciendo lo mismo.
    years_since_last_promotion INT,  -- Años que han pasado desde su último ascenso.
    years_with_curr_manager INT,     -- Tiempo trabajando bajo su jefe actual.

    -- =========================================================================
    -- 8. CONDICIONES LABORALES
    -- Detalles finales sobre su jornada de trabajo.
    -- =========================================================================
    over_time VARCHAR(10),           -- Indica si suele trabajar horas extra.
    standard_hours INT               -- Horas que debe cumplir por contrato.
);