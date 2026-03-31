/*******************************************************************************
Título: Visualización Preliminar de Empleados
Objetivo: Obtener una muestra rápida de los datos almacenados en la tabla final 
          de empleados.
Descripción: Este script selecciona todos los campos de la tabla 'employee_final' 
             y limita el resultado a los primeros 10 registros para verificar 
             la estructura y calidad de los datos sin cargar toda la tabla.
*******************************************************************************/

-- Selecciona todas las columnas (*) de la tabla principal de empleados
SELECT * 
-- Indica la fuente de datos (tabla employee_final)
FROM employee_final
-- Limita la visualización solo a los primeros 10 registros
LIMIT 10;



/*******************************************************************************
Título: Detección de Empleados Duplicados
Objetivo: Identificar inconsistencias en la base de datos de empleados.
Descripción: Este script analiza la tabla 'employee_final' para encontrar
             números de empleado que aparecen más de una vez, lo que indica
             registros duplicados que deben ser revisados.
*******************************************************************************/

SELECT 
    -- Selecciona el número de empleado para identificarlo
    employee_number,    
    -- Cuenta cuántas veces aparece cada número de empleado
    COUNT(*) AS repeticiones
-- Define la tabla de origen de los datos
FROM employee_final
-- Agrupa los resultados por número de empleado para poder contarlos
GROUP BY employee_number
-- Filtra y muestra solo aquellos grupos con más de un registro (duplicados)
HAVING COUNT(*) > 1;



/*******************************************************************************
TITULO: Consolidación y Validación de Empleados Activos
OBJETIVO: Obtener una vista completa de los empleados, uniendo información
          de departamentos y puestos, asegurando la calidad de los datos.
DESCRIPCIÓN: Este script combina la tabla principal de empleados (employee_final)
             con los catálogos de departamentos y puestos para obtener nombres
             legibles en lugar de IDs. Además, filtra los registros para asegurar
             que la información tenga un mínimo de calidad (datos esenciales).
*******************************************************************************/

SELECT
    e.employee_number,
    d.department_name,
    jr.job_role_name,
    e.monthly_income
FROM employee_final e
-- Une la tabla de empleados con el catálogo de departamentos para obtener el nombre del área
JOIN department_catalog d ON e.department_id = d.department_id
-- Une con el catálogo de puestos para obtener el nombre del rol laboral
JOIN job_role_catalog jr ON e.job_role_id = jr.job_role_id
-- CRITERIOS DE VALIDACIÓN: Filtra para mantener registros con información mínima necesaria
WHERE
    -- 1. Verifica que el empleado tenga un número de identificación asignado
    e.employee_number IS NOT NULL OR
    -- 2. Verifica que el empleado esté vinculado a un departamento conocido
    d.department_name IS NOT NULL OR
    -- 3. Verifica que el empleado tenga un puesto de trabajo definido
    jr.job_role_name IS NOT NULL OR
    -- 4. Verifica que exista información sobre su salario mensual
    e.monthly_income IS NOT NULL;




/*******************************************************************************
TITULO: Auditoría de Datos de Empleados - Reporte de Errores
OBJETIVO: Identificar registros de empleados que contienen información incompleta
          o ilógica en los campos de departamento y sueldo mensual.
DESCRIPCIÓN: Este script consulta la tabla final de empleados para localizar
             filas donde el departamento esté vacío o el ingreso mensual sea
             cero o negativo, permitiendo la depuración de datos.
*******************************************************************************/

SELECT
    e.employee_number,      -- Número de identificación único del colaborador
    d.department_name,      -- Nombre del área de trabajo
    e.monthly_income        -- Salario mensual registrado
FROM employee_final e        -- Tabla principal que contiene la información de los empleados
JOIN department_catalog d ON e.department_id = d.department_id -- Vincula el empleado con su departamento
-- CRITERIOS DE ERROR: Se seleccionan registros que cumplen condiciones ilógicas
WHERE
    -- 1. Identificar departamentos vacíos (texto sin contenido, por ejemplo: '')
    d.department_name = '' OR
    -- 2. Identificar salarios no válidos (cero o negativos)
    e.monthly_income <= 0;



/*******************************************************************************
TITULO: Conteo Total de Empleados
OBJETIVO: Obtener el número total de registros en la tabla de empleados.
DESCRIPCION: Este script realiza una consulta rápida para conocer el volumen
             actual de empleados censados en el sistema.
*******************************************************************************/

SELECT
    COUNT(*) -- Cuenta el total de filas (registros) en la tabla, incluyendo nulos
FROM
    employee_final; -- Especifica la tabla principal que contiene el censo de empleados



/*******************************************************************************
TITULO: Reporte de Conteo de Empleados por Departamento
OBJETIVO: Obtener el número total de empleados que trabajan en cada área de la empresa.
DESCRIPCIÓN: Este script consulta la tabla de empleados, la relaciona con el 
             catálogo de departamentos para obtener el nombre real de cada área, 
             y realiza un conteo agrupado para mostrar el total de personal por 
             departamento.
********************************************************************************/

SELECT
    -- Selecciona el nombre del departamento de la tabla relacionada (d)
    d.department_name,   
    -- Cuenta el total de empleados (filas) agrupados por departamento
    COUNT(*) AS total_empleados
-- Selecciona la tabla de empleados como fuente principal (alias e)
FROM employee_final e
-- Une con el catálogo de departamentos (alias d) usando el ID compartido
JOIN department_catalog d ON e.department_id = d.department_id
-- Agrupa el conteo anterior según el nombre del departamento
GROUP BY d.department_name;