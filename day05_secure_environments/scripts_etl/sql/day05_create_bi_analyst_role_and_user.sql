/*******************************************************************************
Título: Configuración de Acceso para Analista BI

Objetivo: Crear un usuario específico para análisis de datos con permisos limitados 
de lectura sobre la tabla de empleados.

Descripción: Este script automatiza la creación de un rol de seguridad, asigna 
permisos de lectura (SELECT) a dicho rol, crea un nuevo usuario y lo asocia al rol 
para garantizar acceso seguro.

Archivo SQL: day05_create_bi_analyst_role_and_user.sql

Archivo PNG: day05_create_bi_analyst_role_and_user_01.png
             day05_create_bi_analyst_role_and_user_02.png
             day05_create_bi_analyst_role_and_user_03.png
             day05_create_bi_analyst_role_and_user_04.png
*********************************************************************************/

-- 1. Crear el rol (perfil) que agrupará los permisos de BI
CREATE ROLE bi_analyst_role;

-- 2. Asignar permiso de lectura (SELECT) sobre la tabla de empleados a este rol
GRANT SELECT ON employee_master_data TO bi_analyst_role;

-- 3. Crear el usuario físico que utilizará el analista
CREATE USER bi_user WITH PASSWORD 'password_seguro';

-- 4. Asignar el rol creado al usuario (hereda los permisos de lectura)
GRANT bi_analyst_role TO bi_user;