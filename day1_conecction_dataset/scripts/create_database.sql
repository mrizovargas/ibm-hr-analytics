/*
================================================================================
TÍTULO: INICIALIZACIÓN DEL ENTORNO DE DATOS - IBM HR ANALYTICS
================================================================================

OBJETIVO: 
Crear el contenedor principal (base de datos) para el almacenamiento de la 
información de Recursos Humanos de IBM.

DESCRIPCIÓN DEL OBJETIVO: 
Este es el primer paso del flujo de trabajo. Consiste en definir un espacio 
lógico aislado y nombrado dentro del servidor de bases de datos, donde se 
alojarán todas las tablas, dimensiones y vistas relacionadas con el análisis 
de capital humano.
*/

-- Definición del contenedor de datos
-- Creamos la base de datos con un nombre descriptivo que indica el origen (IBM) 
-- y el propósito (HR Analytics).
CREATE DATABASE ibm_hr;

-- NOTA OPERATIVA: Una vez creada, asegúrate de activar la base de datos 
-- (Set as default) para que todas las tablas posteriores se guarden en este proyecto.
