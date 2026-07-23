/***************************************************************************************************
Título: CONTROL DE CALIDAD DE DATOS - CONTEO DE INTEGRIDAD EN COMBINACIÓN DE EMPLEADOS

Objetivo: Medir el volumen final de registros tras acoplar empleados y sus puestos.

Descripción: Este script calcula el total de trabajadores que tienen un puesto válido asignado en el 
sistema. Sirve como control matemático: si este número es menor al total original de empleados, 
confirma una pérdida silenciosa de registros debido a códigos de puesto erróneos o vacíos.

Archivo SQL: day16_count_joined_employees.sql

Archivo PNG: day16_count_joined_employees.png
*****************************************************************************************************/

-- 1. Contamos el total de filas que resulten tras aplicar el filtro de cruce de información.
SELECT COUNT(*) AS total_registros_combinados

-- 2. Tomamos como punto de partida la lista principal con los datos diarios de los empleados.
FROM fact_employees AS e

-- 3. Conectamos con el catálogo maestro de puestos para traer la información detallada.
INNER JOIN dim_jobs AS d
    
    -- 4. Regla de unión: solo emparejamos si el código de puesto coincide exactamente en ambos lados.
    ON e.job_id = d.job_id;