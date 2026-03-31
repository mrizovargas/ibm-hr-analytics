/*******************************************************************************
Título: Visualización Preliminar de Datos Maestros de Empleados
Objetivo: Obtener una muestra rápida de los datos almacenados en la tabla 
          principal de empleados.
Descripción: Selecciona las primeras 10 filas de la tabla 'employee_master_data'
             para verificar la estructura, el tipo de datos y la calidad de la
             información sin cargar toda la base de datos.
*******************************************************************************/

-- Selecciona todas las columnas (*) de la tabla especificada
SELECT * 
-- Define la tabla de origen de los datos
FROM employee_master_data
-- Limita el resultado a solo las primeras 10 filas para una vista rápida
LIMIT 10;



/*******************************************************************************
TÍTULO: Detección de Duplicados en Maestro de Empleados
OBJETIVO: Identificar números de empleado que aparecen más de una vez en la tabla
          maestra para asegurar la integridad de los datos.
DESCRIPCIÓN: Este script consulta la tabla principal de empleados, agrupa por el
             identificador único y filtra aquellos grupos que tienen un conteo
             superior a 1, indicando una duplicidad de registros.
*******************************************************************************/

SELECT
    -- Selecciona el identificador del empleado
    employee_number,
    -- Cuenta cuántas veces aparece cada número para identificar el total de duplicados
    COUNT(*) AS repeticiones
-- Define la tabla de origen de datos maestros de empleados
FROM employee_master_data
-- Agrupa los resultados por número de empleado para consolidar el conteo
GROUP BY employee_number
-- Filtro final: Solo muestra los números de empleado cuyo conteo sea mayor a 1
HAVING COUNT(*) > 1;



/*******************************************************************************
TITULO: Depuración de Maestros de Empleados
OBJETIVO: Obtener una lista limpia de colaboradores desde la tabla maestra.
DESCRIPCIÓN: Selecciona todos los registros de 'employee_master_data' que tengan
             información crítica mínima, excluyendo registros donde el ID,
             departamento, puesto o salario estén vacíos (NULL).
********************************************************************************/

SELECT  *
-- Tabla fuente con la información cruda de los colaboradores
FROM employee_master_data
-- CRITERIOS DE VALIDACIÓN: El registro debe tener contenido en AL MENOS
-- uno de estos campos para ser considerado válido y útil.
WHERE
    employee_number IS NOT NULL OR -- 1. Que el ID de empleado esté definido.
    department      IS NOT NULL OR -- 2. Que el departamento tenga un nombre asignado.
    job_role        IS NOT NULL OR -- 3. Que el puesto de trabajo esté definido.
    monthly_income  IS NOT NULL;   -- 4. Que exista un registro del salario mensual.


    
/*******************************************************************************
TITULO: Detección de Colaboradores con Datos Incompletos o Inválidos
OBJETIVO: Identificar empleados en la tabla maestra que carecen de área asignada
          o que tienen un sueldo ilógico (cero o negativo).
DESCRIPCIÓN: Este script consulta la base de datos de RRHH para encontrar
             registros con errores críticos en 'departamento' o 'ingreso mensual'
             que requieren corrección.
*******************************************************************************/

SELECT
    employee_number, -- Identificador único del colaborador
    department,      -- Área asignada (se busca si está vacía)
    monthly_income   -- Sueldo registrado (se busca si es incorrecto)
-- Tabla principal que contiene la información de RRHH
FROM employee_master_data
-- CRITERIOS DE ERROR: Filtra registros con problemas de calidad de datos
WHERE
    department = '' OR -- Error 1: Departamento vacío (texto sin contenido)
    monthly_income <= 0; -- Error 2: Salario cero o negativo (valor ilógico)




/*******************************************************************************
 TÍTULO: Conteo Total de Empleados
 
 OBJETIVO:
 Obtener el número total de registros en la tabla maestra de empleados.
 
 DESCRIPCIÓN:
 Esta consulta cuenta todas las filas existentes en la tabla 'employee_master_data',
 lo que representa el censo total de empleados registrados en el sistema,
 independientemente de si tienen datos nulos o no.
*******************************************************************************/

SELECT
    -- Cuenta todas las filas, incluyendo valores nulos si los hubiera.
    COUNT(*)
-- Tabla maestra principal que contiene el censo de empleados.
FROM employee_master_data;



/*******************************************************************************
TITULO: Reporte de Conteo de Empleados por Departamento
OBJETIVO: Obtener el total de empleados activos agrupados por su área funcional.
DESCRIPCIÓN: Este script consulta la tabla maestra de empleados para sumar cuántos
             empleados pertenecen a cada departamento, permitiendo visualizar la
             distribución del personal.
*******************************************************************************/

SELECT
    -- Selecciona la columna del departamento para identificar el grupo
    department,
    -- Cuenta el número total de filas (empleados) dentro de cada grupo
    COUNT(*) AS total_empleados
-- Define la tabla principal donde se almacena la información de los empleados
FROM employee_master_data
GROUP BY
    -- Agrupa los resultados por departamento para que el conteo no sea global,
    -- sino específico para cada área definida en la tabla.
    department;