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
	e.employee_number,    
	-- Cuenta cuántas veces aparece cada número de empleado
	COUNT(*) AS repeticiones
	-- Define la tabla de origen de los datos
FROM employee_final AS e
-- Agrupa los resultados por número de empleado para poder contarlos
GROUP BY e.employee_number
-- Filtra y muestra solo aquellos grupos con más de un registro (duplicados)
HAVING COUNT(*) > 1;



/*******************************************************************************
Título: Consolidación y Validación de Empleados Activos

Objetivo: Obtener una vista completa de los empleados, uniendo información 
de departamentos y puestos, asegurando la calidad de los datos.

Descripción: Este script combina la tabla principal de empleados (employee_final) 
con los catálogos de departamentos y puestos para obtener nombres 
legibles en lugar de IDs. Además, filtra los registros para asegurar 
que la información tenga un mínimo de calidad (datos esenciales).
*******************************************************************************/

SELECT
	e.employee_number,      -- Número único de identificación del empleado
	dc.department_name,    -- Nombre del departamento (obtenido del catálogo)
	jrc.job_role_name,     -- Nombre del puesto de trabajo (obtenido del catálogo)
	e.monthly_income-- Salario mensual del empleado
FROM employee_final AS e
-- Une la tabla de empleados con el catálogo de departamentos para obtener el nombre del área
JOIN department_catalog AS dc ON e.department_id = dc.department_id
-- Une con el catálogo de puestos para obtener el nombre del rol laboral
JOIN job_role_catalog AS jrc ON e.job_role_id = jrc.job_role_id
-- CRITERIOS DE VALIDACIÓN: Filtra para mantener registros con información mínima necesaria
WHERE
	-- 1. Verifica que el empleado tenga un número de identificación asignado
	e.employee_number IS NOT NULL OR
	-- 2. Verifica que el empleado esté vinculado a un departamento conocido
	dc.department_name IS NOT NULL OR
	-- 3. Verifica que el empleado tenga un puesto de trabajo definido
	jr.job_role_name IS NOT NULL OR
	-- 4. Verifica que exista información sobre su salario mensual
	e.monthly_income IS NOT NULL;



/*******************************************************************************
Título: Identificación de Registros de Empleados con Datos Incompletos o Inválidos

Objetivo: Detectar empleados cuyo nombre de departamento no esté definido (vacío/nulo) 
o que tengan un ingreso mensual nulo o no positivo (<= 0).

Descripción: Este script cruza la tabla de empleados con la de departamentos para 
obtener los nombres de los departamentos y filtra aquellos registros que presentan 
inconsistencias en el nombre del departamento o en el monto de ingresos.
*******************************************************************************/

SELECT
	e.employee_number,      -- Selecciona el número identificador único del empleado
	dc.department_name,     -- Selecciona el nombre del departamento asociado
	e.monthly_income-- Selecciona el ingreso mensual del empleado
FROM
	employee_final AS e-- Tabla principal de empleados (alias 'e')
JOIN
	department_catalog AS dc-- Une con la tabla catálogo de departamentos (alias 'dc')
	ON e.department_id = dc.department_id-- Cruza las tablas usando el ID de departamento
WHERE
	-- Filtro de Calidad de Datos:
	-- 1. dc.department_name: Comprueba si es nulo, vacío ('') o espacios en blanco
	-- 2. e.monthly_income: Comprueba si el ingreso es 0 o menor (inválido)
	(TRIM(COALESCE(dc.department_name, '')) = ''
	OR e.monthly_income <= 0);



/*******************************************************************************
Título: Conteo Total de Empleados

Objetivo: Obtener el número total de registros en la tabla de empleados.

Descripción: Este script realiza una consulta rápida para conocer el volumen 
actual de empleados censados en el sistema.
*******************************************************************************/

SELECT
	COUNT(*) -- Cuenta el total de filas (registros) en la tabla, incluyendo nulos
FROM
	employee_final;-- Especifica la tabla principal que contiene el censo de empleados



/*******************************************************************************
Título: Reporte de Conteo de Empleados por Departamento

Objetivo: Obtener el número total de empleados que trabajan en cada área de la empresa.

Descripción: Este script consulta la tabla de empleados, la relaciona con el 
catálogo de departamentos para obtener el nombre real de cada área, 
y realiza un conteo agrupado para mostrar el total de personal por 
departamento.
********************************************************************************/

SELECT
	-- Selecciona el nombre del departamento de la tabla relacionada (d)
	dc.department_name,   
	-- Cuenta el total de empleados (filas) agrupados por departamento
	COUNT(*) AS total_empleados
-- Selecciona la tabla de empleados como fuente principal (alias e)
FROM employee_final AS e
-- Une con el catálogo de departamentos (alias d) usando el ID compartido
JOIN department_catalog AS dc ON e.department_id = dc.department_id
-- Agrupa el conteo anterior según el nombre del departamento
GROUP BY dc.department_name;