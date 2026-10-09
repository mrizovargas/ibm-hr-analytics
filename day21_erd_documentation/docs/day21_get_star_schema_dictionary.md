|tabla|columna|tipo_dato|permite_null|tipo_restriccion|
|-----|-------|---------|------------|----------------|
|dim_demographics|sk_demographics_id|bigint|NO|PRIMARY KEY|
|dim_demographics|gender|character varying|NO|ATTRIBUTE|
|dim_demographics|education_field|character varying|NO|ATTRIBUTE|
|dim_demographics|marital_status|character varying|NO|ATTRIBUTE|
|dim_jobs|sk_job_id|bigint|NO|PRIMARY KEY|
|dim_jobs|job_id|bigint|NO|ATTRIBUTE|
|dim_jobs|job_role|character varying|NO|ATTRIBUTE|
|dim_jobs|department|character varying|NO|ATTRIBUTE|
|dim_jobs|standard_hours|integer|NO|ATTRIBUTE|
|dim_jobs|is_active|boolean|NO|ATTRIBUTE|
|dim_jobs|high_turnover_risk|character varying|YES|ATTRIBUTE|
|fact_employees|sk_employee_id|bigint|NO|PRIMARY KEY|
|fact_employees|employee_number|integer|NO|ATTRIBUTE|
|fact_employees|sk_job_id|bigint|NO|FOREIGN KEY|
|fact_employees|sk_demographics_id|bigint|NO|FOREIGN KEY|
|fact_employees|attrition_numeric|integer|NO|ATTRIBUTE|
|fact_employees|attrition|character varying|NO|ATTRIBUTE|
|fact_employees|monthly_income|numeric|NO|ATTRIBUTE|
|fact_employees|years_at_company|integer|NO|ATTRIBUTE|
|fact_employees|total_working_years|integer|NO|ATTRIBUTE|
