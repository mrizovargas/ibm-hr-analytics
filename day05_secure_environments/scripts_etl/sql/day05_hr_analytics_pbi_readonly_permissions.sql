/*******************************************************************************
Título: Configuración de Acceso para Power BI (HR Analytics)

Objetivo: Crear un usuario seguro y permisos de "solo lectura" para que Power BI 
se conecte a la base de datos de recursos humanos.

Descripción: Este script elimina configuraciones previas, crea un rol con permisos 
limitados, crea el usuario final y lo asigna a dicho rol.

Archivo SQL: day05_hr_analytics_pbi_readonly_permissions.sql

Archivo PNG: day05_hr_analytics_pbi_readonly_permissions_01.png
             day05_hr_analytics_pbi_readonly_permissions_02.png
             day05_hr_analytics_pbi_readonly_permissions_03.png
             day05_hr_analytics_pbi_readonly_permissions_04.png
             day05_hr_analytics_pbi_readonly_permissions_05.png
             day05_hr_analytics_pbi_readonly_permissions_06.png
             day05_hr_analytics_pbi_readonly_permissions_07.png
*********************************************************************************/

-- 1. Limpieza inicial: Eliminamos el usuario si ya existía para evitar errores
--    de "usuario duplicado" al ejecutar el script de nuevo.
DROP USER IF EXISTS pbi_user;

-- 2. Creación del Rol: Creamos un rol (grupo de permisos) diseñado para
--    ser utilizado por la herramienta Power BI.
CREATE ROLE powerbi_reader;

-- 3. Permisos de Conexión: Permitimos al rol conectarse a la base de datos
--    específica de 'ibm_hr_analytics'.
GRANT CONNECT ON DATABASE ibm_hr_analytics TO powerbi_reader;

-- 4. Permisos de Esquema: Damos permiso de uso (USAGE) sobre el esquema 'public',
--    lo que permite al usuario ver la estructura, pero no modificarla.
GRANT USAGE ON SCHEMA public TO powerbi_reader;

-- 5. Permisos de Lectura: Otorgamos permiso para consultar (SELECT) datos
--    específicamente en la tabla 'employee_master_data'.
GRANT SELECT ON employee_master_data TO powerbi_reader;

-- 6. Creación del Usuario: Creamos el usuario 'pbi_user' con su contraseña.
CREATE USER pbi_user WITH PASSWORD 'SecurityPass2026';

-- 7. Asignación de Rol: Asignamos el rol creado anteriormente al usuario,
--    heredando así todos los permisos de lectura configurados.
GRANT powerbi_reader TO pbi_user;

