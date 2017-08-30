




# How many people participated in p2_second_interview? Get PID
SELECT project_id
FROM subjects_ids
WHERE unique_id in (SELECT unique_id FROM p2_second_interviews);

# get primary key of table in question
SELECT column_name
FROM   information_schema.key_column_usage
WHERE  table_schema = schema()             -- only look in the current db
AND    constraint_name = 'PRIMARY'         -- always 'PRIMARY' for PRIMARY KEY constraints
AND    table_name = 'p2_second_interviews';    -- specify your table.