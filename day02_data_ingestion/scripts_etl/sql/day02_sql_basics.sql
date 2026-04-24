/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 01: SELECT
*******************************************************************************/

/*******************************************************************************
Título: Reporte de Empleados Senior
 
Objetivo: Identificar a los empleados con una edad superior a 50 años.
 
Descripción: Este script selecciona el número de empleado, su edad y su puesto
de trabajo de la tabla maestra de empleados, filtrando únicamente aquellos cuya
edad sea mayor a 50 años para análisis de talento senior.

Resultado CSV: day02_senior_empl_over_50.csv
*******************************************************************************/
 
-- Selecciona los datos necesarios de la tabla maestra de empleados.
SELECT
	e.employee_number, -- Identificador único del empleado
	e.age,             -- Edad actual del empleado
	e.job_role-- Puesto o rol que desempeña
FROM
	employee_master_data AS e
WHERE
	e.age > 50-- Filtra solo a empleados con edad mayor a 50 años
ORDER BY
	e.age DESC;-- Ordena resultados de mayor a menor edad



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 02: SELECT
*******************************************************************************/

/*******************************************************************************
Título: Extracción de Datos Maestros de Empleados para Evaluación

Objetivo: Obtener información clave de los empleados para analizar su desempeño
en relación con sus ingresos mensuales.

Descripción: El script selecciona el número de empleado, su ingreso mensual y
su calificación de desempeño actual desde la tabla maestra.

Resultado CSV: day02_empl_performance_vs_income.csv
*******************************************************************************/

-- Selecciona las columnas específicas: id del empleado, sueldo y nota de desempeño
SELECT
	e.employee_number,    -- Identificador único del empleado
	e.monthly_income,     -- Salario base mensual
	e.performance_rating-- Calificación del desempeño actual
FROM
	employee_master_data AS e;-- Tabla origen con la información maestra de empleados



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 03: SELECT
*******************************************************************************/

/*******************************************************************************
Título: Análisis de Rotación por Departamento y Puesto

Objetivo: Identificar los niveles de rotación de personal (attrition)
desglosados por departamento y rol laboral.

Descripción: Este script extrae datos de la tabla maestra de empleados para
mostrar qué departamentos y puestos específicos están experimentando
salidas de personal, permitiendo analizar tendencias de retención.

Resultado CSV: day02_empl_attrition_by_dept.csv
*******************************************************************************/

-- Selecciona las columnas clave: Departamento, Puesto y Estado de Rotación
SELECT
	e.department,   -- Nombre del área funcional
	e.job_role,     -- Puesto específico del empleado
	e.attrition-- Indicador de si el empleado se fue (Sí/No)
FROM
	employee_master_data AS e;-- Tabla origen con la información consolidada de empleados



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 01: WHERE
*******************************************************************************/

/*******************************************************************************
Título: Análisis de Empleados con Rotación (Attrition)
 
Objetivo: Identificar qué empleados han abandonado la empresa para facilitar 
estudios sobre las causas de la rotación de personal.
 
Descripción: Este script selecciona el número de empleado, su departamento y 
el estado de rotación de la tabla 'employee_master_data', filtrando únicamente 
a aquellos que han abandonado la compañía ('Yes').

Resultado CSV: day02_attrition_cases_by_dept.csv
********************************************************************************/

-- Selecciona las columnas clave para identificar al empleado y su área
SELECT
	e.employee_number, -- Identificador único del empleado
	e.department,      -- Área a la que pertenece
	e.attrition-- Indica si el empleado se fue (Yes/No)
FROM
	employee_master_data AS e-- Tabla principal de datos maestros de empleados
WHERE
	e.attrition = 'Yes';-- Filtra para mostrar solo a quienes abandonaron la empresa



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 02: WHERE
*******************************************************************************/

/*******************************************************************************
Título: Análisis de Empleados con Salario Alto y Baja Satisfacción

Objetivo: Detectar perfiles que ganan más de 5000 (unidad monetaria)
pero tienen una puntuación de satisfacción laboral inferior a 2 (baja),
posiblemente para evaluar riesgo de fuga o mejorar el clima laboral.

Descripción: Este script selecciona el número de empleado, su ingreso mensual 
y su nivel de satisfacción laboral de la tabla maestra de empleados.

Resultado CSV: day02_empl_retention_risk.csv
*******************************************************************************/

-- Seleccionamos los datos relevantes del empleado
SELECT
	e.employee_number,   -- Número identificador único del empleado
	e.monthly_income,    -- Ingreso mensual para identificar el nivel de salario
	e.job_satisfaction-- Nivel de satisfacción (usado para detectar riesgo de fuga)
FROM
	employee_master_data AS e-- Buscamos en la tabla maestra de empleados
WHERE
	e.monthly_income > 5000-- FILTRO 1: Empleados con sueldo superior a 5000
	AND e.job_satisfaction < 2;-- FILTRO 2: Solo aquellos con baja satisfacción (1 o 0)



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 03: WHERE
*******************************************************************************/

/*******************************************************************************
Título: Extracción de Empleados del Área de Ciencias de la Vida

Objetivo: Obtener una lista de empleados que cuentan con formación académica
en el campo de 'Life Sciences'.
          
Descripción: Este script consulta la tabla maestra de empleados para filtrar
y seleccionar los números de identificación y el campo de estudio
de aquellos cuyo perfil educativo sea 'Life Sciences'.

Resultado CSV: day02_life_sciences_talent_pool.csv
********************************************************************************/

-- Selecciona las columnas identificador del empleado y campo educativo
SELECT
	e.employee_number, 
	e.education_field
FROM
	-- De la tabla principal de datos maestros de empleados
	employee_master_data AS e
-- Filtra para incluir solamente a empleados con estudios en 'Life Sciences'
WHERE
	e.education_field = 'Life Sciences';



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 01: ORDER BY
*******************************************************************************/

/*******************************************************************************
Título: Reporte de Ingresos Mensuales por Empleado

Objetivo: Identificar a los empleados con mayores ingresos mensuales.

Descripción: Este script consulta la base de datos maestra de empleados para
obtener su número de identificación y su sueldo mensual, ordenando
los resultados de mayor a menor ingreso para visualizar a los empleados mejor
pagados primero.

Resultado CSV: day02_empl_monthly_income_ranking.csv
********************************************************************************/

-- Selección de columnas: Número de empleado e ingresos mensuales
SELECT
	e.employee_number,
	e.monthly_income
-- Origen de datos: Tabla maestra de empleados
FROM
	employee_master_data AS e
-- Ordenamiento: De mayor a menor (DESC) basado en el salario
ORDER BY
	e.monthly_income DESC;



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 02: ORDER BY
*******************************************************************************/

/*******************************************************************************
 Título: Análisis de Antigüedad de Empleados
 
 Objetivo: Identificar y ordenar a los empleados según su tiempo de permanencia en la empresa
 para visualizar quiénes son los más recientes.
 
 Descripción: Este script consulta la base de datos maestra de empleados para extraer el número
 de identificación y los años de servicio, ordenando los resultados de forma
 ascendente (de menor a mayor antigüedad).
 
 Resultado CSV: day02_empl_years_at_company_ranking.csv
*******************************************************************************/

-- Selecciona las columnas necesarias: identificación del empleado y años en la empresa
SELECT
	e.employee_number, 
	e.years_at_company
-- Desde la tabla principal de datos maestros de empleados
FROM
	employee_master_data AS e
-- Ordena los resultados por años de antigüedad (ascendente: menor a mayor)
ORDER BY
	e.years_at_company ASC;



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 03: ORDER BY
*******************************************************************************/

/*******************************************************************************
  Título: Análisis de Satisfacción Laboral
  
  Objetivo: Identificar a los empleados con mayores niveles de satisfacción laboral.
  
  Descripción: Este script consulta la base de datos maestra de empleados para extraer 
  el número de empleado y su puntuación de satisfacción, ordenándolos
  de mayor a menor para destacar a los más satisfechos.
  
  Resultado CSV: day02_empl_job_satisfaction_ranking.csv
*******************************************************************************/

-- Selecciona las columnas necesarias: número de empleado y nivel de satisfacción
SELECT
	e.employee_number, 
	e.job_satisfaction
FROM
	employee_master_data AS e-- Indica la tabla de origen con los datos maestros
ORDER BY
	e.job_satisfaction DESC;-- Ordena los resultados de manera descendente (mayor a menor)



/*******************************************************************************
Día 2 - 120      Diccionario Técnico Operativo       Caso 01:  PRIMARY KEY (PK)
*******************************************************************************/

/*******************************************************************************
Título: Detección de Empleados Duplicados

Objetivo: Identificar registros duplicados en la tabla maestra de empleados.

Descripción: Este script escanea la tabla 'employee_master_data' para encontrar
números de empleado que aparecen más de una vez, lo que indica una posible
duplicidad de datos que debe ser corregida.

Resultado CSV: day02_duplicate_empl_records_audit.csv
********************************************************************************/

-- Seleccionamos el número de empleado y contamos cuántas veces aparece cada uno.
SELECT
	e.employee_number, 
	COUNT(*) AS total_registros
FROM
	employee_master_data AS e-- Buscamos en la tabla maestra de empleados.
GROUP BY
	e.employee_number-- Agrupamos los datos por cada número de empleado único.
HAVING
	COUNT(*) > 1;-- Filtramos para mostrar solo los grupos con más de un registro.