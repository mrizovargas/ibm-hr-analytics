/**********************************************************************************
Título: Creación de Vista Centralizada para el Manejo de Nulos

Objetivo: Construir una vista limpia y estandarizada de los datos de los empleados.

Descripción: Este script crea (o actualiza) una Vista (VIEW), que funciona como una 
tabla virtual. Su propósito es tomar la información de la tabla original de datos 
brutos y aplicar reglas automáticas para rellenar campos vacíos en dos áreas clave: 
los ingresos mensuales (se vuelven 0) y la calificación de desempeño (se vuelve 99). 
De esta forma, cualquier reporte futuro puede consultar esta vista directamente sin 
preocuparse por los datos faltantes.

Archivo SQL: day11_create_view_clean_null_handling.sql

Archivo PNG: day11_create_view_clean_null_handling.png
**************************************************************************************/

-- BLOQUE DE CREACIÓN: Define la estructura de la tabla virtual (Vista).
-- Si la vista ya existía, 'OR REPLACE' la borra y la vuelve a crear con los cambios nuevos.
CREATE OR REPLACE VIEW view_clean_null_handling AS 

	-- BLOQUE DE SELECCIÓN Y TRANSFORMACIÓN: Extrae y limpia las columnas necesarias.
	SELECT 
		-- Identificador único del empleado en el sistema.
		employee_id,
		
		-- Número de nómina o identificación oficial de la empresa.
		employee_number,
		
		-- Departamento al que pertenece el empleado (ej. Ventas, TI, RH).
		department,
		
		-- Puesto o rol específico que desempeña el trabajador.
		job_role,
		
		-- Control de ingresos: Si el salario está vacío, lo convierte en 0. 
		-- Guarda el resultado bajo el nuevo nombre 'clean_monthly_income'.
		COALESCE(monthly_income, 0) AS clean_monthly_income,
		
		-- Control de calificación: Si el desempeño está vacío, le asigna un 99.
		-- El '99' se usa como un código visual para identificar "Empleado Sin Evaluación".
		COALESCE(performance_rating, 99) AS clean_performance_rating
        
	-- BLOQUE DE ORIGEN: Indica la procedencia de la información.
	FROM
		-- Tabla principal que contiene el histórico de datos brutos y desorganizados.
		employee_master_dirty_data;