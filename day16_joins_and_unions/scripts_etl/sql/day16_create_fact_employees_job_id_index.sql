/***********************************************************************************
 Título: Creación de índice para optimizar búsquedas por puesto de trabajo

 Objetivo: Acelerar la velocidad de respuesta al consultar empleados según su puesto.

 Descripción: Genera una estructura de acceso rápido sobre la columna del puesto de 
 trabajo en la tabla de empleados, evitando que el sistema tenga que revisar la tabla 
 completa en cada consulta.

 Archivo SQL: day16_create_fact_employees_job_id_index.sql
***********************************************************************************/

-- ====================================================================================
-- BLOQUE 1: CREACIÓN DEL ÍNDICE DE OPTIMIZACIÓN
-- Objetivo: Crear una guía de localización rápida para la columna de puestos
-- ====================================================================================

-- Creamos un "índice" (similar al índice de un libro) llamado 'idx_fact_empl_job_id'.
-- Esto le enseña a la base de datos dónde está exactamente la información de cada puesto.
CREATE INDEX idx_fact_employees_job_id
-- Indicamos que este acceso rápido se guardará en la tabla principal de empleados ('fact_employees')
-- tomando como referencia los códigos de puesto ('job_id').
ON fact_employees(job_id);