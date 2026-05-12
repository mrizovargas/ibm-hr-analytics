/*******************************************************************************
 Título: Limpieza de Datos Maestros de Empleados
 
 Objetivo:
 Eliminar de forma rápida y definitiva todos los registros existentes en la tabla 
 'employee_master_data' para asegurar que esté vacía antes de un proceso de carga
 o actualización masiva.
 
 Descripción:
 Este script utiliza la sentencia TRUNCATE, la cual es más eficiente que DELETE 
 para vaciar tablas, ya que no registra la eliminación fila por fila, sino que 
 libera el espacio de almacenamiento de inmediato y reinicia los contadores de 
 identidad (si los hay).
 
 Archivo SQL: day02_truncate_empl_mstr_data_tbl.sql
 
 Archivo PNG: day02_truncate_empl_mstr_data_tbl.png
********************************************************************************/

-- Ejecuta la eliminación total de los datos en la tabla especificada.
TRUNCATE TABLE employee_master_data;
