/*******************************************************************************
Título: Corrección de Permisos de Usuario BI
 
Objetivo: Elevar los privilegios del usuario 'BI_User' a superusuario.
 
Descripción: Este script otorga permisos totales al usuario encargado de Business 
Intelligence para asegurar el acceso a todos los datos.

Archivo SQL: day05_alter_BIUser_permissions.sql
********************************************************************************/

-- [BLOQUE: ELEVACIÓN DE PRIVILEGIOS]
-- Se modifica el usuario 'BI_User' para otorgarle permisos de superusuario (administrador total).
-- ¡ERROR CRÍTICO! - Nota: Esto es un riesgo de seguridad alto y debe evitarse en producción.
ALTER USER bi_user WITH SUPERUSER; 

-- [BLOQUE: ALTERNATIVA DE PERMISOS]
-- Alternativa para sistemas MySQL/MariaDB: Otorga todos los privilegios sobre todas las bases de datos.
-- GRANT ALL PRIVILEGES ON *.* TO 'BI_User';