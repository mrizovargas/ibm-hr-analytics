/***********************************************************************************
 * Título: Validación de Dependencias Funcionales y Reglas de Integridad
 * 
 * Objetivo: Detectar violaciones lógicas en la relación entre puestos y áreas.
 * 
 * Descripción: Este script audita la tabla plana para verificar si el puesto de 
 * trabajo (job_role) determina de forma única a su departamento (department). Si la 
 * consulta devuelve algún registro, significa que la regla matemática X --> Y se ha 
 * roto (un mismo puesto tiene dos o más departamentos asignados), alertándonos de un 
 * error de diseño.
 *
 * Arcivo SQL: day15_validate_functional_dependencies.sql
 * 
 * Archivo CSV: day15_validate_functional_dependencies.csv
 * 
 * Archivo PNG: day15_validate_functional_dependencies.png
 ***********************************************************************************/

-- Iniciamos la selección indicando las columnas que queremos analizar y contar
SELECT 
    job_role, -- El puesto de trabajo que queremos evaluar como determinante (X).
    
    -- Contamos cuántos departamentos únicos e independientes tiene asociados cada puesto.
    -- Al usar DISTINCT, evitamos contar el mismo departamento múltiples veces.
    COUNT(DISTINCT department) 

-- Especificamos la tabla original denormalizada donde residen los datos maestros
FROM employee_master_data

-- Agrupamos la información fila por fila usando el nombre del puesto de trabajo.
-- Esto consolida todos los registros repetidos en un único renglón analítico por puesto.
GROUP BY job_role

-- Aquí ocurre la magia del filtro: solo mostramos los puestos que rompieron la regla.
-- Si el conteo final es estrictamente mayor a 1, significa que encontramos una falla:
-- ¡el puesto de trabajo NO determina funcionalmente a su departamento!
HAVING COUNT(DISTINCT department) > 1;