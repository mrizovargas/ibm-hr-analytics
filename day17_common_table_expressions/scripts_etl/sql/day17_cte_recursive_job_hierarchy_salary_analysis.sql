/*************************************************************************************
 Título: Análisis Jerárquico Recursivo de Sueldos por Nivel y Departamento

 Objetivo: Generar una vista organizada de los sueldos promedio por puesto y área.

 Descripción: Primero calcula el sueldo promedio de cada puesto por departamento. 
 Luego, mediante un proceso recursivo, recorre nivel por nivel (del 1 al 5) para 
 conectar la estructura organizacional y ordenar los ingresos de mayor a menor.

 Archivo SQL: day17_cte_recursive_job_hierarchy_salary_analysis.sql

 Archivo CSV: day17_cte_recursive_job_hierarchy_salary_analysis.csv

 Archivo PNG: day17_cte_recursive_job_hierarchy_salary_analysis.png
*************************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CÁLCULO PREVIO DE PROMEDIOS POR PUESTO Y DEPARTAMENTO
-- Objetivo: Agrupar la información base para evitar repetir cálculos en la recursión
-- ====================================================================================

WITH RECURSIVE base_promedios AS (
    SELECT 
        -- Número del 1 al 5 que indica la posición del puesto en la empresa
        job_level,
        -- Área o departamento al que pertenece el empleado
        department,
        -- Nombre del puesto o función específica
        job_role,
        -- Calculamos el salario promedio mensual del puesto en ese departamento
        AVG(monthly_income) AS salario_promedio
    FROM 
        -- Consultamos la tabla principal con todos los expedientes del personal
        employee_master_data
    WHERE 
        -- Aseguramos incluir solo registros válidos dentro del rango de niveles 1 a 5
        job_level IS NOT NULL AND job_level BETWEEN 1 AND 5
    GROUP BY 
        -- Agrupamos para obtener una sola fila por departamento, nivel y puesto
        department,
        job_level, 
        job_role
),

-- ====================================================================================
-- BLOQUE 2: CONSTRUCCIÓN RECURSIVA DE LA ESTRUCTURA ORGANIZACIONAL
-- Objetivo: Recorrer paso a paso la jerarquía conectando el Nivel 1 hasta el Nivel 5
-- ====================================================================================

jerarquia_puestos AS (
    -- MIEMBRO ANCLA: Tomamos como punto de partida únicamente los puestos de Nivel 1
    SELECT 
        job_level,
        department,
        job_role,
        salario_promedio,
        -- Asignamos la posición inicial de nuestra escala jerárquica
        1 AS nivel_jerarquico
    FROM 
        base_promedios
    WHERE 
        job_level = 1

    UNION ALL

    -- MIEMBRO RECURSIVO: Avanzamos al siguiente nivel sumando 1 en cada iteración
    SELECT 
        b.job_level,
        b.department,
        b.job_role,
        b.salario_promedio,
        -- Incrementamos en una unidad el escalón jerárquico actual
        j.nivel_jerarquico + 1 AS nivel_jerarquico
    FROM 
        base_promedios AS b
    -- Cruzamos la tabla de promedios con la lista que estamos construyendo
    INNER JOIN 
        jerarquia_puestos AS j 
        ON b.job_level = j.job_level + 1
    WHERE 
        -- Ponemos un límite para detener el proceso al llegar al nivel 5
        j.nivel_jerarquico < 5
)

-- ====================================================================================
-- BLOQUE 3: PRESENTACIÓN Y FORMATO FINAL DE LOS RESULTADOS
-- Objetivo: Redondear montos monetarios y ordenar la lista para su análisis
-- ====================================================================================

SELECT DISTINCT 
    -- Escalón asignado durante el recorrido paso a paso
    nivel_jerarquico,
    -- Nivel original registrado en los datos del empleado
    job_level,
    -- Departamento al que pertenece el puesto
    department,
    -- Nombre exacto del rol o puesto de trabajo
    job_role,
    -- Convertimos el promedio a número estándar y lo redondeamos a dos decimales
    ROUND(salario_promedio::numeric, 2) AS sueldo_promedio_nivel
FROM 
    -- Consultamos el resultado final generado por la estructura recursiva
    jerarquia_puestos
ORDER BY 
    -- Muestra primero los niveles más bajos (1) y avanza hasta los superiores (5)
    nivel_jerarquico ASC,
    -- Dentro de cada nivel, muestra arriba los puestos con mejor sueldo
    sueldo_promedio_nivel DESC;