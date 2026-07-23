/*******************************************************************************
 * Título: Consulta de Empleados del Departamento de Ventas
 * 
 * Objetivo: Extraer y ordenar el perfil de los vendedores según sus ingresos.
 * 
 * Descripción: 
 * - Selecciona datos clave de los empleados.
 * - Filtra únicamente al personal del departamento de Ventas.
 * - Ordena la lista de forma descendente, empezando por el ingreso más alto.
 *
 * Archivo SQL: day16_sales_employees_revenue.sql
 *
 * Archivo CSV: day16_sales_employees_revenue.csv
 *
 * Archivo PNG: day16_sales_employees_revenue.png
 ******************************************************************************/

SELECT 
    f.employee_number AS id_empleado,    -- Etiqueta el número del empleado como "id_empleado"
    f.age AS edad,                       -- Etiqueta la edad del empleado como "edad"
    f.monthly_income AS ingreso_mensual, -- Etiqueta su sueldo mensual como "ingreso_mensual"
    j.job_role AS puesto,                -- Etiqueta el título del cargo como "puesto"
    j.department AS departamento         -- Etiqueta el área de trabajo como "departamento"
FROM 
    fact_employees AS f                  -- Extrae datos desde la tabla de empleados llamándola "f"
INNER JOIN 
    dim_jobs AS j                        -- Une esta información con la tabla de puestos llamándola "j"
ON 
    f.job_id = j.job_id                  -- Conecta ambas tablas usando el código de puesto como puente
WHERE 
    j.department = 'Sales'               -- Filtra los registros para mostrar solo a los de Ventas
ORDER BY 
    f.monthly_income DESC;               -- Ordena el resultado de mayor a menor ingreso mensual
