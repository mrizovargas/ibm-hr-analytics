/***********************************************************************************
 * Título: Script de Validación Cruzada e Integridad Financiera (Post-Migración)
 * 
 * Objetivo: Auditar y certificar que la migración dimensional fue 100% exitosa.
 * 
 * Descripción: Este script ejecuta tres pruebas críticas de control de calidad sobre
 * nuestro nuevo modelo. Primero, cuenta los registros totales; segundo, rastrea 
 * posibles filas huérfanas (sin conexión); y tercero, compara las sumas salariales 
 * exactas entre el origen plano y el destino en la tabla de hechos para garantizar 
 * que no hubo pérdidas ni alteraciones.
 *
 *Archivo SQL: day15_audit_fact_employees_integrity.sql
 *
 *Archivo PNG: day15_audit_fact_employees_integrity_1.png
 *			   day15_audit_fact_employees_integrity_2.png
 *			   day15_audit_fact_employees_integrity_3.png
 ***********************************************************************************/

-- ---------------------------------------------------------------------------------
-- BLOQUE 1: CONTEO TOTAL DE REGISTROS (CROSS-FIELD VALIDATION)
-- ---------------------------------------------------------------------------------

-- Contamos cuántos empleados quedaron registrados en nuestra nueva tabla central.
-- Si todo salió bien, este número debe coincidir con el volumen del archivo original.
SELECT COUNT(*)
FROM fact_employees;


-- ---------------------------------------------------------------------------------
-- BLOQUE 2: DETECCIÓN DE REGISTROS HUÉRFANOS (INTEGRIDAD REFERENCIAL)
-- ---------------------------------------------------------------------------------

-- Buscamos empleados que se hayan quedado sin un puesto asignado en la migración.
-- Filtramos las filas donde 'job_id' esté vacío (IS NULL). El resultado ideal es 0.
SELECT COUNT(*)
FROM fact_employees
WHERE job_id IS NULL;


-- ---------------------------------------------------------------------------------
-- BLOQUE 3: VALIDACIÓN CRUZADA DE TOTALES FINANCIEROS (CONCORDANCIA ECONÓMICA)
-- ---------------------------------------------------------------------------------

-- Comparamos la suma global de dinero de ambas tablas para ver si los datos coinciden.
SELECT
    -- Subconsulta 1: Sumamos todos los salarios mensuales en la nueva tabla de hechos.
    (SELECT SUM(monthly_income)
     FROM fact_employees) AS total_destino,
  
     -- Subconsulta 2: Sumamos los mismos salarios en la tabla plana original de origen.
    (SELECT SUM(monthly_income)
     FROM employee_master_data) AS total_origen;