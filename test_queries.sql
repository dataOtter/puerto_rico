USE puerto_rico;

SHOW TABLES;

DROP DATABASE puerto_rico;

SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA='puerto_rico' 
    AND TABLE_NAME='subjects_ids';

# get primary key of table in question
SELECT column_name
FROM   information_schema.key_column_usage
WHERE  table_schema = schema()             -- only look in the current db
AND    constraint_name = 'PRIMARY'         -- always 'PRIMARY' for PRIMARY KEY constraints
AND    table_name = 'p2_second_interviews';    -- specify your table.


# ALL P1 -- 315
#SELECT DISTINCT project_id FROM p1_screenings;
create view all_p1 as SELECT DISTINCT project_id, rds_id FROM p1_screenings;
# ALL P2 -- 119
#SELECT DISTINCT project_id FROM subjects_ids WHERE unique_id IN (SELECT unique_id FROM p2_network_interviews);
SELECT DISTINCT project_id FROM subjects_ids WHERE unique_id IN (SELECT unique_id FROM p2_network_interviews);
# ALL that were in P1 and/or P2 (union) -- 353 = (315+119)-81 -- (ALLP1+ALLP2)-P1ANDP2
SELECT DISTINCT project_id FROM all_p1 
UNION 
SELECT DISTINCT project_id FROM all_p2;
# ALL that were in P1 AND P2 (intersection) -- 81
SELECT DISTINCT project_id FROM p1_p2_overlaps;

# all men in p1(315) -- 285
select distinct project_id from p1_screenings where rds_id in (select rds_id from p1_interviews where GEN = 1);
# all men in p2(119) -- 106
select distinct project_id from all_men 
where project_id in (select project_id from all_p2);
# all men in p1 and/or p2 (union, 353) -- 318, females 32, transgender 1
create view all_men as SELECT DISTINCT project_id FROM subjects_ids
WHERE project_id IN (SELECT project_id FROM p1_screenings WHERE rds_id IN (SELECT rds_id FROM p1_interviews WHERE GEN = 1))  # all men from p1
OR project_id IN (SELECT project_id FROM p2_first_interviews WHERE P2FIGEN = 1);  # all men new in p2
# all men in p1 AND p2 (intersection, 81) -- 73, females 7, transgender 1
SELECT distinct project_id FROM p1_p2_overlaps 
WHERE rds_id IN (SELECT rds_id FROM p1_interviews WHERE GEN = 1);


# age range
SET @min_age = 20;
SET @max_age = 31;
# all is 51
SELECT DISTINCT project_id FROM subjects_ids 
WHERE (project_id IN (SELECT DISTINCT project_id FROM p1_screenings WHERE EP2 >= @min_age AND EP2 <= @max_age)
OR project_id IN (SELECT DISTINCT project_id FROM p2_first_interviews WHERE P2FIAGE >= @min_age AND P2FIAGE <= @max_age))
# WHAT??????
AND project_id IN (SELECT project_id FROM p2_first_interviews) OR rds_id IN (SELECT rds_id FROM p2_second_interviews); -- all p2 78

#AND project_id IN (SELECT project_id FROM p2_first_interviews); -- p2 only 6
#AND project_id IN (SELECT project_id FROM p1_screenings); -- all p1 45
#AND project_id IN (SELECT project_id FROM p1_p2_overlaps); -- intersection 8
#AND project_id IN (SELECT project_id FROM p1_screenings) AND rds_id NOT IN (SELECT rds_id FROM p2_second_interviews); -- p1 only 37






 
