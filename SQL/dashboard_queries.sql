use puerto_rico;

show tables;

SELECT 
    SUM(EP2 < 30) AS 'in 20s',
    SUM(29 < EP2 AND EP2 < 40) AS 'in 30s',
    SUM(39 < EP2 AND EP2 < 50) AS 'in 40s',
    SUM(49 < EP2) AS '50+',
    DM1
FROM
    p1_screenings
        INNER JOIN
    p1_interviews ON p1_screenings.rds_id = p1_interviews.rds_id
GROUP BY DM1;
    
SELECT 
    SUM(P2FIAGE < 30) AS 'in 20s',
    SUM(29 < P2FIAGE AND P2FIAGE < 40) AS 'in 30s',
    SUM(39 < P2FIAGE AND P2FIAGE < 50) AS 'in 40s',
    SUM(49 < P2FIAGE) AS '50+',
    P2FIDM1
FROM
    p2_first_interviews
GROUP BY P2FIDM1;
    

    
    
    
    
    