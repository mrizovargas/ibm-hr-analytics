/*******************************************************************************
Título: Segmentación de Empleados por Banda Salarial

Objetivo: Clasificar al personal según sus ingresos mensuales.

Descripción: El script consulta la tabla maestra de empleados para extraer sus 
datos básicos de identificación, puesto y departamento. Adicionalmente, calcula 
y asigna una categoría salarial (Alto, Medio o Bajo) a cada empleado para 
facilitar análisis internos.

Archivo SQL: day10_employee_salary_segmentation.sql

Archivo CSV: day10_employee_salary_segmentation.csv

Archivo PNG: day10_employee_salary_segmentation.png
*********************************************************************************/

-- Bloque de selección: Extrae la información básica y calcula la banda salarial
SELECT 
    employee_id,      -- Identificador único interno de cada empleado
    employee_number,  -- Número de nómina o registro visible del trabajador
    department,       -- Área o departamento donde labora
    job_role,         -- Puesto o rol que desempeña actualmente
    monthly_income,   -- Monto bruto del salario mensual

    -- Lógica de clasificación salarial paso a paso:
    CASE 
        -- Si gana más de 10,000, se etiqueta como ingresos altos
        WHEN monthly_income > 10000 THEN 'Alto'
        
        -- Si gana entre 5,001 y 10,000, se etiqueta como ingresos medios
        WHEN monthly_income > 5000 THEN 'Medio'
        
        -- Para cualquier cantidad menor o igual a 5,000, se etiqueta como ingresos bajos
        ELSE 'Bajo' 
    END AS salary_band -- Guarda el resultado anterior en una nueva columna llamada 'salary_band'

-- Origen de los datos:
FROM 
    employee_master_data; -- Indica que toda la información se extrae de la tabla maestra de empleados

	