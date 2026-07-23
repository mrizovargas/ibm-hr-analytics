/************************************************************************************
 * Título: Creación de Tabla Plana Ineficiente (Demostración de Redundancia)
 *
 * Objetivo: Diseñar una tabla denormalizada para el registro maestro de empleados.
 * 
 * Descripción: Este script define una estructura inicial "plana" donde se guardan 
 * tanto los datos del empleado como los de su puesto y departamento el problema de 
 * la redundancia masiva de datos (Sirve como el contraejemplo perfecto para ilustrar 
 * horas estándar repetido para 3,000 personas) antes de normalizar.
 * 
 * Archivo SQL: day15_create_denormalized_employee_table.sql
 ************************************************************************************/

-- Primero, creamos la estructura que almacenará de golpe toda la información
CREATE TABLE employee_master_data (
    
    -- Identificador único para cada trabajador. Es nuestra llave primaria (PRIMARY KEY),
    -- lo que significa que no se puede repetir y nos sirve para ubicar a cada persona.
    employee_number INT PRIMARY KEY,
    
    -- Nombre del puesto o rol que desempeña el empleado (por ejemplo: 'Sales Executive').
    -- Usamos VARCHAR(100) para permitir textos descriptivos de hasta 100 caracteres.
    job_role VARCHAR(100),
    
    -- Departamento al que pertenece el puesto (por ejemplo: 'Sales' o 'R&D').
    -- Al estar en la misma tabla, este texto se escribirá una y otra vez por cada empleado.
    department VARCHAR(100),
    
    -- Cantidad de horas laborales estándar establecidas para el puesto de trabajo.
    -- ¡Ojo aquí! Este valor numérico se repetirá idénticamente para los 3,000 empleados,
    -- lo que genera un desperdicio innecesario de almacenamiento en el disco duro.
    standard_hours INT
);