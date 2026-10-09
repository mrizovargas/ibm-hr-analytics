### 🔗 Mapeo de Capa Lógica en Tableau Desktop

*El modelo utiliza la **capa lógica** de **Tableau** para preservar la **granularidad nativa** del dataset **'IBM HR Analytics Employee Attrition & Performance'**, evitando la **duplicación sintética de filas** al calcular **ingresos** o **promedios**.*

| Tabla Origen (Fact) | Campo Clave (Fact) | Tabla Dimensión | Campo Clave (Dim) | Tipo de Relación |
|---|---|---|---|---|
| **fact_employees** | `sk_job_id` | **dim_jobs**| `sk_job_id`| Capa Lógica (Noodle / Many-to-One) |
| **fact_employees** | `sk_demographic_id` | **dim_demographics**| `sk_demographic_id`| Capa Lógica (Noodle / Many-to-One) |