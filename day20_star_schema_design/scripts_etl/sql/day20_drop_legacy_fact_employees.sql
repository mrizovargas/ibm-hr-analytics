/*******************************************************************************
 Título: Eliminación de la Tabla de Hechos Legacy de Empleados (fact_employees)

 Objetivo: Eliminar del esquema la tabla previa de hechos fact_employees tras 
 haber migrado exitosamente las métricas a la nueva estructura.

 Descripción: Ejecuta la eliminación condicional de la tabla de hechos obsoleta 
 para liberar espacio y mantener un modelo de datos limpio sin redundancias.

 Archivo SQL: day20_drop_legacy_fact_employees.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: ELIMINACIÓN DE LA TABLA OBSOLETA
-- Objetivo: Remover la estructura previa de hechos si existe en la base de datos.
-- ====================================================================================

DROP TABLE IF EXISTS fact_employees;                         -- Elimina la tabla de hechos legacy