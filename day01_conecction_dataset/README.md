# Día 1: Conexión y Estructuración del Dataset IBM HR

**Autor:** Miguel Angel Rizo Vargas  
**Fecha de inicio:** 24 de marzo de 2026

Este módulo documenta la fase inicial del proyecto, donde se estableció la infraestructura de datos necesaria, priorizando la **seguridad** y la **integridad de la información** desde el origen.

---

## Objetivo
Configurar el entorno de datos conectando el dataset de IBM HR a **PostgreSQL**, crear la base de datos `ibm_hr`, definir la tabla maestra `employee_master_data` y validar la carga inicial de los registros.

---

## Pasos Realizados

1.  **Configuración de Entorno Seguro:** Implementación de `python-dotenv` para gestionar credenciales de base de datos sin exponer datos sensibles en el código fuente.
2.  **Modelado en PostgreSQL:** Creación de la base de datos `ibm_hr` y la tabla `employee_master_data` utilizando una nomenclatura estricta en `snake_case` para asegurar la compatibilidad con herramientas de análisis.
3.  **Ingesta de Datos:** Importación del dataset original (CSV) hacia PostgreSQL mediante:
        a. El **asistente de importación en DBeaver**:  Herramienta gráfica que permite cargar datos desde archivos externos (CSV, Excel, SQL, etc.) hacia tablas de bases de datos existentes o nuevas, facilitando la asignación de columnas, configuración de formatos y tipos de datos, simplificando migraciones y actualizaciones.
        b. **Pipeline de Python optimizado**, mediante el uso de librerías (pandas, csv, numpy).
4.  **Auditoría de Calidad (Data Quality):** Validación de la carga mediante consultas SQL de control:
    * Detección de registros duplicados (`HAVING COUNT(*) > 1`)
    * Detección de registros nulos (`IS NOT NULL`)
    * Detección de registros vacíos o fuera de rango (`columna_nombre1 = '' OR columna_nombre2 <=0 `)
    * Verificación de volumen (`COUNT(*)`).
    * Muestreo de integridad (`SELECT * LIMIT 10`).
    * Análisis de distribución inicial por departamento.
5.  **Documentación Técnica:** Generación del esquema **Entity-Relationship (ER)** para visualizar la estructura de los datos.

---

## Stack Tecnológico
* **Lenguaje:** Python 3.10+ (Pandas, Psycopg2).
* **Base de Datos:** PostgreSQL 14+.
* **Gestión de Entorno:** VS Code & `.env` secrets.

---

## Evidencias del Proceso
Para mayor detalle, puedes consultar los archivos técnicos en las siguientes rutas:
- Scripts SQL en `/scripts_etl/sql/` (ej. create_db.sql, create_table.sql).
- Scripts Python en `/scripts_etl/scr/` (ej. normalize_dataset.py,sql_extract_raw_data.py).
- Documentación en `/docs/` (ej. er_diagram.pdf).
- Resultados de queries en `/results/` (ej. query_validation.csv).
- Imágenes/Capturas de pantalla en `/results/screenshots/` (ej. ibm_hr_erd.png).

---

## Insight Inicial
El dataset **IBM HR** ha quedado correctamente estructurado y limpio, quedando listo para responder preguntas de negocio sobre **rotación (attrition)**, **niveles de ingresos** y **desempeño laboral**. Esta base sólida garantiza que todos los análisis y modelos posteriores sean confiables y precisos.

---