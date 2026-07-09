/*********************************************************************************
 * Título: Actualización de Infraestructura - Renombre de Columna de Costos
 * 
 * Objetivo: Modificar de forma permanente el nombre de la columna 'daily_rate' en
 * la tabla.
 * 
 * Decripción: Este script de lenguaje de definición de datos (DDL) es ejecutado 
 * por el equipo de TI/Sistemas. Su propósito es cambiar el nombre físico de la 
 * columna 'daily_rate' a 'costo_diario_operativo' en la tabla maestra de 
 * empleados. Este cambio busca estandarizar la nomenclatura del negocio al español
 * o adaptar el modelo a nuevas reglas de infraestructura, asegurando la integridad
 * de los tipos de datos preexistentes.
 * 
 * Archivo SQL: day13_alter_emp_master_rename_daily_rate.sql
 *********************************************************************************/

-- Modifica la estructura de la tabla maestra para aplicar cambios en sus columnas.
ALTER TABLE employee_master_data
	-- Renombra de forma definitiva el campo original al nuevo estándar operativo.
	RENAME COLUMN daily_rate TO costo_diario_operativo;