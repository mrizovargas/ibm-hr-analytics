/*******************************************************************************
Título: Auditoría y Control de Calidad de Valores Nulos

Objetivo: Validar que la vista de datos limpios no contenga ningún valor vacío.

Descripción: Este script actúa como una prueba de control de calidad (Quality 
Assurance). Su función es contar si todavía queda algún registro con valores 
nulos (vacíos) en las columnas críticas de ingresos ('clean_monthly_income') o 
de desempeño ('clean_performance_rating') dentro de la vista que creamos 
previamente. El resultado ideal de este script siempre debería ser cero (0).

Archivo SQL: day11_check_null_values_in_view.sql

Archivo PNG: day11_check_null_values_in_view.png
*************************************************************************************/

-- BLOQUE DE CONTEO: Define la métrica de auditoría que queremos calcular.
SELECT 
	-- Cuenta el total de filas que cumplen con la condición de error de abajo.
	-- El resultado se guardará en una columna llamada 'nulos_restantes'.
	COUNT(*) AS nulos_restantes 

-- BLOQUE DE ORIGEN: Especifica sobre qué tabla o vista se hará la auditoría.
FROM 
	-- Consultamos la vista estandarizada que ya debería tener los datos limpios.
	view_clean_null_handling

-- BLOQUE DE CONDICIÓN (FILTRO): Especifica las reglas de búsqueda de fallas.
WHERE 
	-- Condición 1: Busca si el ingreso mensual se quedó vacío por error...
	clean_monthly_income IS NULL OR 
    
	-- Condición 2: ...o si la calificación de desempeño se quedó vacía.
	clean_performance_rating IS NULL;
	