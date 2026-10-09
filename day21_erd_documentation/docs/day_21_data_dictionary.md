## Diccionario de Datos del Modelo

| Tabla | Columna | Tipo de Dato | Permite Nulos |
|---|---|---|---|
| **dim_demographics** | `sk_demographics_id` | `bigint` | NO |
| **dim_demographics** | `gender` | `character varying` | NO |
| **dim_demographics** | `education_field` | `character varying` | NO |
| **dim_demographics** | `marital_status` | `character varying` | NO |
| **dim_jobs** | `sk_job_id` | `bigint` | NO |
| **dim_jobs** | `job_id` | `bigint` | NO |
| **dim_jobs** | `job_role` | `character varying` | NO |
| **dim_jobs** | `department` | `character varying` | NO |
| **dim_jobs** | `standard_hours` | `integer` | NO |
| **dim_jobs** | `is_active` | `boolean` | NO |
| **dim_jobs** | `high_turnover_risk` | `character varying` | YES |
| **fact_employees** | `sk_employee_id` | `bigint` | NO |
| **fact_employees** | `employee_number` | `integer` | NO |
| **fact_employees** | `sk_job_id` | `bigint` | NO |
| **fact_employees** | `sk_demographics_id` | `bigint` | NO |
| **fact_employees** | `attrition_numeric` | `integer` | NO |
| **fact_employees** | `attrition` | `character varying` | NO |
| **fact_employees** | `monthly_income` | `numeric` | NO |
| **fact_employees** | `years_at_company` | `integer` | NO |
| **fact_employees** | `total_working_years` | `integer` | NO |
