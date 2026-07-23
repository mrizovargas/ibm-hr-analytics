/*******************************************************************************
 * Título: Consulta de ingresos de empleados por puesto y departamento
 * 
 * Objetivo: Cruzar los ingresos del personal con sus roles organizacionales.
 * 
 * Descripción: Junta la base de datos de salarios con la lista de puestos 
 * empleando el código de trabajo, permitiendo ver el dinero ganado por cada 
 * número de empleado junto a su área de trabajo.
 *
 * Archivo SQL: day16_salary_and_role_join.sql
 *
 * Archivo PNG: day16_salary_and_role_join.png
 ******************************************************************************/

SELECT 
    e.employee_number, -- Trae el número único de identificación de cada empleado.
    e.monthly_income,  -- Extrae el sueldo mensual bruto registrado del trabajador.
    d.job_role,        -- Obtiene el nombre del puesto que ocupa la persona.
    d.department       -- Identifica el área o departamento al que pertenece.
FROM 
    fact_employees AS e -- Usa la tabla de nómina/empleados y la apoda 'e'.
LEFT JOIN 
    dim_jobs AS d       -- Conecta la tabla de puestos de trabajo y la apoda 'd'.
ON 
    e.job_id = d.job_id; -- Une ambas tablas usando el código de puesto idéntico.
