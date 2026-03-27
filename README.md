# IBM HR Analytics Employee Attrition & Performance


## 📖 Descripción del Proyecto
Este proyecto de **People Analytics** transforma datos de Recursos Humanos en decisiones estratégicas. Utilizando el dataset de **IBM HR**.

---

## 🎯 Objetivos del Proyecto
1. **Predicción de riesgo de rotación**: Desarrollar **modelos de clasificación** (ej. **Regresión Logística** o **Random Forest**) para asignar una **probabilidad de abandono** a cada empleado, facilitando **intervenciones proactivas**.

2. **Análisis de compromiso (Engagement)**: Investigar cómo la **satisfacción laboral** (JobSatisfaction), el **entorno** (EnvironmentSatisfaction) y el **equilibrio vida-trabajo** (WorkLifeBalance) impactan en la **intención de permanencia**.

3. **Optimización de compensaciones**: Analizar la relación entre el **salario mensual** (MonthlyIncome), **aumentos** (PercentSalaryHike), **opciones de acciones** (StockOptionLevel) y la **rotación** para mejorar la estructura retributiva.

4. **Evaluación de equidad y diversidad demográfica**: Analizar la **rotación** y **satisfacción** desglosadas por **género, nivel educativo, edad y estado civil** para detectar **sesgos** o **patrones de desigualdad**.

5. **Análisis de desarrollo y antigüedad**: Estudiar la influencia de los **años en la empresa** (YearsAtCompany), **años desde la última promoción** (YearsSinceLastPromotion) y el **nivel del puesto** (JobLevel) en la **retención**.

6. **Impacto de la carga laboral**: Evaluar la correlación entre las **horas extras** (OverTime) y el **desgaste** o **rotación** del personal.

7. **Segmentación de perfiles y ubicación**: Analizar la **distancia al hogar** (DistanceFromHome), el **departamento** (Department) y el **rol laboral** (JobRole) para personalizar las **estrategias de retención**.

8. **Segmentación de Fuerza Laboral**: Agrupación de empleados por **perfiles** (clusters) para detectar qué **departamentos** o **niveles jerárquicos** presentan un mayor **riesgo de desmotivación**.

9. **Predicción de Desempeño**: Identificación de las **variables clave** (como años bajo el mismo gerente o formación) que impulsan el **alto rendimiento**.

---

## 📊 Dataset
*   **Fuente:** Creado por científicos de datos de IBM (Ficticio).
*   **Registros:** 1,470 empleados.
*   **Columnas:** 35 variables (demográficas, satisfacción, rendimiento, condiciones de trabajo).
*   **Variable Objetivo:** `Attrition` (Yes/No).

---

### Variables Clave
*   **Demográficas:** Age, Gender, MaritalStatus.
*   **Trabajo:** Department, JobRole, JobLevel, JobSatisfaction, EnvironmentSatisfaction.
*   **Compensación:** MonthlyIncome, PercentSalaryHike, StockOptionLevel.
*   **Trayectoria:** YearsAtCompany, YearsInCurrentRole, TotalWorkingYears.

---

## 🛠️ Estructura del Repositorio

DM_Roadmap_P1_120D/
│
├── 01_strategy/		# Documentación estratégica (ej. PDF): roadmap del proyecto, definición de KPIs, business case y justificación de valor.
├── 02_data/           		# Contiene todos los datos del proyecto, organizados por estado de procesamiento.
│   ├── raw/        		# Datos originales sin modificar (CSV, JSON, SQL dumps, APIs, fuentes externas).
│       ├── rrhh/
│           ├── WA_Fn-UseC_-HR-Employee-Attrition.csv           # Dataset original.
│   ├── processed/  		# Datos finales listos para modelado, BI o dashboards (limpios y transformados).
│   └── interim/       		# Datos intermedios: parcialmente transformados, aún no aptos para modelado/BI.
│
├── 03_scripts_etl/		# Código para extracción, transformación y carga (ETL).
│   ├── src/			# Scripts en Python para pipelines reutilizables y producción. reutilizables.
│   │	├── data_loader.py	# ej. Script para conectar y extraer datos desde SQL u otras fuentes.
│   │	└── feature_eng.py	# ej. Script para ingeniería de características (creación de nuevas variables).
│   └── sql/			# Código SQL para gestión de tablas y consultas.
│    	├── create_tables.sql	# ej. Script de creación de tablas en la base de datos.
│    	└── queries.sql		# ej. Consultas SQL para extracción y análisis.
│
├── 04_exploration_eda/		# Exploración inicial de datos y prototipado.
│   └── notebooks/		# Jupyter Notebooks para análisis exploratorio y pruebas rápidas.
│    	├── 01-eda.ipynb	# ej. Notebook de EDA: gráficas, outliers, correlaciones.
│    	└── 02-modelado.ipynb	# ej. Notebook de prototipado de modelos iniciales.
│
├── 05_reports			# Reportes generados: análisis en CSV, PDF, HTML, imágenes, etc.
│   └── figures/		# # Gráficos y visualizaciones (PNG, PDF, HTML) exportadas para informes finales.
│
├── 06_dashboards/		# Archivos de visualización interactiva (Power BI .pbix, Tableau .twbx).
│
├── 07_workspace/		# Espacio de trabajo temporal (archivos auxiliares, pruebas).
│
├── 08_config/			# Archivos de configuración y credenciales (no subir a Git por seguridad).
│
├── 09_github/			# Evidencia organizada para GitHub (subcarpetas con documentación y resultados).
│   └── ibm-hr-analytics/
│   	└── .gitignore/		# Define qué archivos no deben subirse a Git (datos sensibles, entornos virtuales, credenciales, etc.).
│   	└── day1_conecction_dataset/
│   		└── docs/	# Documentación.
│   		└── results/	# Resultados obtenidos.
│   		└── scripts_etl/	# Código para extracción, transformación y carga (ETL).
│   			└── scr/	# Scripts en Python para pipelines reutilizables y producción.
│   			└── sql/	# Código SQL para gestión de tablas y consultas. reutilizables.
│   		└── README.md		# Guía rápida del subproyecto.
│   	└── README.md			# Descripción general del repositorio.
│
├── 10_docs/			# Documentación adicional (manuales, referencias, papers, etc.).
│
├── README.md           	# Documento principal: explica el propósito del proyecto, objetivos, alcance, guías de uso y cómo reproducir resultados.
├── requirements.txt    	# Lista de dependencias (pip/conda) necesarias para ejecutar el proyecto de forma reproducible.
└──

---

# 🏗️ Arquitectura de la Solución
El proyecto se divide en fases modulares para garantizar la escalabilidad:

1.  **Pipeline de Datos (Python):** Ingesta y normalización de datos crudos aplicando estándares **PEP 8** y seguridad mediante variables de entorno (`.env`).
2.  **Modelado Relacional (PostgreSQL):** Estructuración de la base de datos `ibm_hr` con nombres en `snake_case` para optimizar consultas.
3.  **Data Quality & Audit (SQL):** Implementación de checks de integridad para eliminar duplicados y gestionar valores nulos.
4.  **Visualización Estratégica (Power BI):** Dashboard interactivo para el monitoreo de la fuerza laboral y detección de alertas de rotación.

---

## 🛠️ Herramientas Utilizadas
* **Lenguaje:** Python 3.10+ (Pandas, Psycopg2, Dotenv).
* **Base de Datos:** PostgreSQL.
* **Business Intelligence:** Power BI.
* **Entorno:** VS Code con extensiones de SQL y Jupyter.

---

## 🛡️ Seguridad y Buenas Prácticas
Este repositorio implementa **estándares de grado de producción**:
* **Zero-Hardcoding:** Las credenciales de base de datos se gestionan mediante archivos `.env` (excluidos del control de versiones por seguridad).
* **Clean Code:** Código modularizado en funciones para facilitar el mantenimiento.
* **Documentación:** Cada fase cuenta con su propio detalle técnico y evidencias de ejecución.

---

## 🚀 Análisis Realizado
1.  **Limpieza de Datos:** Eliminación de variables irrelevantes (`EmployeeCount`, `StandardHours`, `Over18`, `EmployeeNumber`).
2.  **EDA:** Visualización de la distribución de retención por género, nivel educativo, ingresos mensuales y satisfacción laboral.
3.  **Preprocesamiento:** Conversión de variables categóricas a numéricas y escalado de datos.
4.  **Modelado:** Aplicación de algoritmos de clasificación (Random Forest, Logistic Regression) para predecir la fuga de talento.

---

## 🚀 Cómo Replicar este Proyecto
1. Clona el repositorio.
2. Crea tu archivo `.env` siguiendo la estructura de `.env.example`.
3. Ejecuta los scripts de la carpeta `/sql/` para preparar tu base de datos local.
4. Corre el script de Python en `/scripts/` para procesar y cargar los datos.

---

## 📈 Insights de Negocio Destacados
* **Análisis por Departamento:** Identificación del área de **Research & Development** como el motor principal de la empresa (961 empleados).
* **Optimización Administrativa:** Evaluación de la carga de trabajo en el equipo de **Sales** y **HR**.
* **Confiabilidad:** 100% de integridad en métricas de ingresos mensuales y roles de trabajo tras la fase de auditoría SQL.

---

## 📧 Contacto
*   **Autor: Miguel Angel Rizo Vargas** - *Ingeniero en Sistemas Computacionales | Especialista en Datos
*   **LinkedIn:** [Tu Perfil]