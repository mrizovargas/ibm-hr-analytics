/*
--------------------------------------------------------------------------------
TÍTULO: Creación de la base de datos para Recursos Humanos de IBM
OBJETIVO: Crear un contenedor lógico (base de datos) para almacenar toda la 
          información relacionada con el personal, departamentos y nómina.
DESCRIPCIÓN: Este script inicializa el entorno de trabajo ejecutando la sentencia
             DDL (Data Definition Language) necesaria para generar el esquema 
             principal de la base de datos 'ibm_hr'.
--------------------------------------------------------------------------------
*/

-- 1. Sentencia principal para crear la base de datos
-- Esta línea genera una nueva base de datos vacía llamada 'ibm_hr'.
CREATE DATABASE ibm_hr;

-- NOTA OPERATIVA: Una vez creada, asegúrate de activar la base de datos 
-- (Set as default) para que todas las tablas posteriores se guarden en este proyecto.
