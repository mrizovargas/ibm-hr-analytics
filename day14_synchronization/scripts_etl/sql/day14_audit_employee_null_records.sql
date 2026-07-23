/****************************************************************************************
 * Título: Auditoría de Registros Huérfanos o Vacíos
 * 
 * Objetivo: Contar cuántos empleados carecen de sus identificadores principales.
 * 
 * Descripción: Este script busca y cuenta aquellos registros en la vista de retención 
 * que no tienen ni 'id_empleado' ni 'num_empleado'. Sirve para detectar fallos en la 
 * carga de datos o registros inválidos que requieran limpieza inmediata.
 *
 * Archivo SQL: day14_audit_employee_null_records.sql 
 *
 * Archivo PNG: day14_audit_employee_null_records.png
 *****************************************************************************************/

-- 1. Iniciamos la función de conteo sobre todo el universo de datos que cumpla con 
--    las condiciones que definiremos más adelante.
SELECT COUNT(*) 

-- 2. Renombramos la columna del resultado final como 'filas_vacias' para que el 
--    usuario final o el analista comprenda de inmediato qué significa este número.
AS filas_vacias

-- 3. Indicamos la fuente de información; en este caso, una vista especializada que 
--    consolida los datos del historial y retención del personal.
FROM view_employee_retention_data

-- 4. Activamos los filtros de búsqueda (la cláusula WHERE) para aislar únicamente 
--    aquellos casos especiales que queremos auditar.
WHERE
	-- Verificamos que el identificador del sistema (ID interno) no exista o esté vacío.
	id_empleado IS NULL 
	
	-- Y ADEMÁS (ambas condiciones deben cumplirse a la vez), confirmamos que tampoco 
	-- exista el número de empleado oficial (el código visible para recursos humanos).
	AND num_empleado IS NULL;