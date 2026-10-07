/*******************************************************************************
 Título: Asignación de Permisos de Lectura para Power BI (pbi_user)

 Objetivo: Otorgar permisos de acceso al usuario de inteligencia de negocios para 
 consultar el esquema público y tablas principales.

 Descripción: Habilita el uso del esquema public y concede accesos de solo lectura 
 (SELECT) a pbi_user sobre las tablas del modelo en estrella.

 Archivo SQL: day20_grant_pbi_user_permissions.sql
*******************************************************************************/

-- ====================================================================================
-- BLOQUE 1: ACCESO AL ESQUEMA PRINCIPAL
-- Objetivo: Permitir al usuario navegar e identificar los objetos del esquema.
-- ====================================================================================

GRANT USAGE ON SCHEMA public TO pbi_user;                    -- Habilita lectura de la estructura public

-- ====================================================================================
-- BLOQUE 2: ACCESO A TABLAS MODELADAS (HECHOS Y DIMENSIONES)
-- Objetivo: Conceder permisos de lectura sobre el modelo de datos estrella.
-- ====================================================================================

GRANT SELECT ON public.fact_employees TO pbi_user;           -- Consulta lectura sobre hechos de empleados
GRANT SELECT ON public.dim_jobs TO pbi_user;                 -- Consulta lectura sobre dimensión de puestos
GRANT SELECT ON public.dim_demographics TO pbi_user;         -- Consulta lectura sobre datos demográficos