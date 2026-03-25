# Día 1 - Conexión al dataset IBM HR

## Objetivo
Conectar el dataset IBM HR a PostgreSQL, crear la base `ibm_hr`, la tabla `employee_master_data` y validar la carga inicial.

## Pasos realizados
1. Creación de la base de datos `ibm_hr`.
2. Creación de la tabla `employee_master_data` con columnas en snake_case.
3. Importación del dataset IBM HR desde CSV.
4. Validación con queries (`SELECT * LIMIT 10`, `COUNT(*)`, distribución por departamento).
5. Generación de esquema ER.

## Evidencias
- Scripts SQL en `/scripts/`.
- Diagrama ER en `/docs/`.
- Resultados de queries y capturas en `/results/`.

## Insight inicial
El dataset IBM HR está listo para responder preguntas de negocio sobre rotación, ingresos y desempeño. La estructura sólida asegura que los análisis posteriores sean confiables.