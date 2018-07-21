USE puerto_rico;

SHOW TABLES;

SELECT filters, length(pids)/6 FROM top_secret_highly_confidential_cheat_sheet order by length(pids) desc;

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

select rds_id from p2_second_interviews;

# ALL P1 -- 315
#SELECT DISTINCT project_id FROM p1_screenings;
create view all_p1 as SELECT DISTINCT project_id, rds_id FROM p1_screenings;
# ALL P2 -- 119
create view all_p2 as SELECT DISTINCT project_id FROM subjects_ids WHERE unique_id IN (SELECT unique_id FROM p2_network_interviews);
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
create view all_women as SELECT DISTINCT project_id FROM subjects_ids
WHERE project_id IN (SELECT project_id FROM p1_screenings WHERE rds_id IN (SELECT rds_id FROM p1_interviews WHERE GEN = 2))  # all women from p1
OR project_id IN (SELECT project_id FROM p2_first_interviews WHERE P2FIGEN = 2);  # all women new in p2
# all men in p1 AND p2 (intersection, 81) -- 73, females 7, transgender 1
SELECT distinct project_id FROM p1_p2_overlaps 
WHERE rds_id IN (SELECT rds_id FROM p1_interviews WHERE GEN = 1);

# age range
SET @min_age = 20;
SET @max_age = 31;
SELECT DISTINCT project_id FROM subjects_ids 
WHERE (project_id IN (SELECT DISTINCT project_id FROM p1_screenings WHERE EP2 >= @min_age AND EP2 <= @max_age)
OR project_id IN (SELECT DISTINCT project_id FROM p2_first_interviews WHERE P2FIAGE >= @min_age AND P2FIAGE <= @max_age)); -- all 51
#AND (project_id IN (SELECT project_id FROM p2_first_interviews) OR rds_id IN (SELECT rds_id FROM p2_second_interviews)); -- all p2 14
#AND project_id IN (SELECT project_id FROM p2_first_interviews); -- p2 only 6
#AND project_id IN (SELECT project_id FROM p1_screenings); -- all p1 45
#AND project_id IN (SELECT project_id FROM p1_p2_overlaps); -- intersection 8
#AND project_id IN (SELECT project_id FROM p1_screenings) AND rds_id NOT IN (SELECT rds_id FROM p2_second_interviews); -- p1 only 37

# minimum drug use per day
SET @p1code = 3;
SET @p2code = 4;
SELECT project_id FROM subjects_ids
WHERE (rds_id IN (SELECT rds_id FROM p1_interviews WHERE ID2 > @p1code)
OR project_id IN (SELECT project_id FROM p2_first_interviews WHERE P2FIID2 > @p2code));

# all male-female relationship edge_ids
SELECT edge_id, sender_pid, receiver_pid FROM edges 
WHERE (sender_pid IN (SELECT * FROM all_men)
AND receiver_pid IN (SELECT * FROM all_women))
OR (sender_pid IN (SELECT * FROM all_women)
AND receiver_pid IN (SELECT * FROM all_men));


# all PR born in p1(315) -- 293
select count(*), DM4 from p1_interviews group by DM4;
select distinct project_id from p1_screenings where rds_id in (select rds_id from p1_interviews where DM4 = 1);

select distinct project_id from subjects_ids where project_id in 
	(select project_id from p1_screenings where rds_id in 
		(select rds_id from p1_interviews where DM4 = 2))
	or project_id in 
		(select project_id from p2_first_interviews where P2FIDM4 = 2);
        
        
# all DR born in p1(315) -- 
select count(*), DM4 from p1_interviews group by DM4;
select distinct project_id from p1_screenings where rds_id in (select rds_id from p1_interviews where DM4 = 3);

select distinct project_id from subjects_ids where project_id in 
	(select project_id from p1_screenings where rds_id in 
		(select rds_id from p1_interviews where DM4 = 3))
	or project_id in 
		(select project_id from p2_first_interviews where P2FIDM4 = 3);


select filters, hash_index, ceil(length(pids)/6), pids from top_secret_highly_confidential_cheat_sheet order by filters;


SELECT DISTINCT
    project_id
FROM
    subjects_ids
WHERE
    (project_id IN (SELECT 
            project_id
        FROM
            p1_screenings
        WHERE
            rds_id IN (SELECT 
                    rds_id
                FROM
                    p1_interviews
                WHERE
                    DM1 = 2))
        OR project_id IN (SELECT 
            project_id
        FROM
            p2_first_interviews
        WHERE
            P2FIDM1 = 2));


########################################################################
# Join all to make one huge table for all pids and related info; and one table for all edge_ids and related info
########################################################################
CREATE OR REPLACE VIEW temp1 AS
    (SELECT 
        project_id AS subject_project_id,
        rds_id AS subjects_rds_id,
        unique_id AS subjects_unique_id
    FROM
        subjects_ids);
        
SELECT 
    s.project_id AS subject_project_id,
    s.rds_id AS subjects_rds_id,
    s.unique_id AS subjects_unique_id,
    ':',
    p1s.intid as `p1s.intid`
FROM
    subjects_ids AS s
        LEFT JOIN
    p1_screenings AS p1s ON s.project_id = p1s.project_id;
    

select * from subjects_ids AS s
	LEFT JOIN p1_screenings AS p1s ON s.rds_id = p1s.rds_id
    left join p1_followups as p1f on s.rds_id = p1f.rds_id
    left join p1_hivs as p1hi on s.rds_id = p1hi.rds_id
    left join p1_hcvs as p1hc on s.rds_id = p1hc.rds_id
    left join p1_interviews as p1i on s.rds_id = p1i.rds_id
    
    left join p2_first_interviews as p2fi on s.unique_id = p2fi.unique_id
    left join p2_second_interviews as p2si on s.unique_id = p2si.unique_id
    left join p2_hivs as p2hi on s.unique_id = p2hi.unique_id
    left join p2_hcvs as p2hc on s.unique_id = p2hc.unique_id;
    
    

SET @sql = CONCAT('SELECT ', (SELECT REPLACE(GROUP_CONCAT(COLUMN_NAME), 'rds_id,' 'project_id,' 'unique_id,', '') 
					FROM INFORMATION_SCHEMA.COLUMNS 
					WHERE TABLE_NAME = 'subjects_all_data' 
					AND TABLE_SCHEMA = 'puerto_rico'), ' FROM subjects_all_data');

PREPARE stmt1 FROM @sql;
EXECUTE stmt1;



#select edge_id, sender_pid, receiver_pid from all_edges_index AS e
select e.*, p2n.*, n.*, r.*, GROUP_CONCAT(en.note_id SEPARATOR ', ') 
from all_edges_index AS e
LEFT JOIN p2_network_supplement_edges AS p2n ON e.edge_id = p2n.edge_id
left join network_edges as n on e.edge_id = n.edge_id
left join rds_edges as r on e.edge_id = r.edge_id
LEFT JOIN edges_to_notes as en ON e.edge_id = en.edge_id
GROUP BY e.edge_id;


SELECT all_edges_index.edge_id, all_edges_index.sender_pid, all_edges_index.receiver_pid, 
GROUP_CONCAT(edges_to_notes.note_id SEPARATOR ', ') AS `note_ids`, 
network_edges.edge_id AS `network_edges.edge_id`, rds_edges.edge_id AS `rds_edges.edge_id` 
FROM all_edges_index 
LEFT JOIN edges_to_notes ON edges_to_notes.edge_id = all_edges_index.edge_id 
LEFT JOIN network_edges ON network_edges.edge_id = all_edges_index.edge_id 
LEFT JOIN rds_edges ON rds_edges.edge_id = all_edges_index.edge_id 
GROUP BY all_edges_index.edge_id;






