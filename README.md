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
├── 01_strategy/           # Fundamentos del proyecto: Roadmap, KPIs, Business Case y justificación del proyecto.
│
├── 02_data/               # Ciclo de vida del dato: Repositorio de datos clasificado por etapas de procesamiento.
│   ├── interim/           # Datos en transformación: Limpieza técnica, normalización y validaciones temporales.
│   ├── processed/         # "Single Source of Truth": Datos finales listos para consumo en modelos de ML o BI.
│   └── raw/               # Solo lectura: Fuentes originales (CSV, JSON, SQL). ¡Prohibido modificar estos archivos!
│
├── 03_scripts_etl/        # Automatización: Motores de procesamiento para mover datos de 'raw' a 'processed'.
│   ├── sql/               # Código SQL para gestión de tablas y consultas.
│   │   ├── create_tables.sql # ej. Estructura y esquemas de tablas.
│   │   └── queries.sql       # ej. Consultas para consumo y análisis avanzado.
│   └── src/               # Código fuente en Python para extracción, limpieza y Feature Engineering.
│   	├── data_loader.py # ej. Conexiones y extracción de fuentes externas o bases de datos.
│	└── feature_eng.py # ej. Creación de nuevas variables y lógica de negocio.
│
├── 04_exploration_eda/    # Laboratorio de experimentación: Sandbox para descubrimiento de patrones y testing.
│   └── notebooks/         # Jupyter Notebooks: Documentación visual de hipótesis, outliers y prototipos.
│       ├── 01_eda.ipynb   # ej. Análisis de calidad de datos, outliers y correlaciones.
│       └── 02_modelado.ipynb # ej. Pruebas preliminares de modelos y algoritmos.
│
├── 05_results/            # Salidas estáticas (CSV): Reportes finales en formato plano divididos por unidad de negocio.
│   ├── bussiness intelligence/ ... sales/ # Segmentación por stakeholder para facilitar la entrega de valor.
│   └── screenshots/   # Evidencias visuales, gráficos clave y diagramas para presentaciones (PNG, PDF, HTML).
│       └── bussiness intelligence/ ... sales/ # Segmentación por stakeholder para facilitar la entrega de valor.
│
├── 06_dashboards/         # Entregables visuales interactivos (archivos .pbix, .twbx o similares).
│   ├── pbi/		   # Archivos binarios de Power BI (.pbix).
│   └── tabl/		   # Archivos binarios de Tableau (.twbx).
│
├── 07_workspace/          # Zona de juegos: Borradores locales y pruebas rápidas. No se sube a producción.
│
├── 08_config/             # Seguridad: Variables de entorno, .env y tokens (excluir de Git por seguridad).
│
├── 09_github/             # Reflejo del repositorio remoto: Estructura pública optimizada para colaboración.
│   └── ibm_hr_analytics/  #Proyecto específico: Aplicación de analítica de RRHH de IBM.
│       ├── .gitignore/    # Filtro de seguridad: Evita la fuga de datos sensibles o archivos pesados (.csv, .log).
│       ├── day1_connection_dataset/	# Onboarding: Guía y scripts para la conexión inicial de datos.
│       │   ├── docs/      # Documentación técnica: Diccionario de datos y diagramas de flujo.
│       │   ├── results/   # Entregables del módulo: Reportes (CSV) y evidencias específicas del día 1.
│       │   │   ├── bussiness intelligence/ ... sales/ # Segmentación por stakeholder para facilitar la entrega de valor.
│       │   │   └── screenshot/	# Evidencias visuales, gráficos clave y diagramas para presentaciones (PNG, PDF, HTML).
│       │   │       └── bussiness intelligence/ ... sales/ # Segmentación por stakeholder para facilitar la entrega de valor.
│       │   │       
│       │   ├── scripts_etl/	# Código para extracción, transformación y carga (ETL).
│       │   │   ├── scr/	# Código fuente en Python para extracción, limpieza y Feature Engineering.
│       │   │   └── sql/	# Código SQL para gestión de tablas y consultas. reutilizables.
│   	│   └── README.md      # Guía del día 1: Contexto específico para el desarrollador del subproyecto.
│       ├── ...            # (Otros días o módulos del proyecto).
│       ├── README.md      # Guía del módulo: Contexto específico para el desarrollador del subproyecto.
│	└── requirements.txt	# Dependencias locales: Listado necesario para replicar el entorno de ejecución.
│
├── 10_docs/               # Biblioteca de referencia: Manuales, material de referencia técnica y especificaciones externas.
│   ├── day1_connection_dataset/ # Módulo inicial: Configuración y carga del dataset.
│   └── ...           	   # (Otros días o módulos del proyecto). 
│
├── README.md              # Carta de presentación: Resumen ejecutivo, guía de instalación y arquitectura.
└── requirements.txt       # Entorno global: Listado necesario para replicar todo el ecosistema del proyecto.

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