/*******************************************************************************
 * Título: Cruce de datos entre información principal y complementaria
 * 
 * Objetivo: Unir dos tablas para consultar y analizar información relacionada.
 * 
 * Descripción: Extrae una columna específica de la primera tabla y la junta con 
 * el dato complementario de la segunda tabla. La unión se realiza utilizando un 
 * identificador idéntico en ambas.
 *
 * Archivo SQL: day16_main_complementary_data_join.sql
 *
 * Archivo PNG: day16_main_complementary_data_join.png
 ******************************************************************************/

SELECT 
    a.columna_1,    -- Extrae una información específica de la primera tabla.
    b.columna2      -- Extrae un dato complementario de la segunda tabla.

FROM 
    taba_a AS a     -- Selecciona la 'tabla_a' y la nombra como 'a' para simplificar.

LEFT JOIN 
    tabla_b AS b    -- Agrega la 'tabla_b' (nombrada como 'b') conectándola a la derecha.

ON 
    a.col_llave_comun = b.col_llave_comun;
                    -- Define el punto de encuentro: busca los datos que comparten
                    -- un mismo identificador exacto en ambas tablas.