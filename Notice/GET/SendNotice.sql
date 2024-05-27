DELIMITER //

CREATE PROCEDURE SendNotice(IN memberEmail VARCHAR(255), IN aircraftName VARCHAR(255), IN roleName VARCHAR(255))
BEGIN
    SELECT DISTINCT email, user_id
    FROM (
        SELECT 
            u.user_id AS user_id,
            r.role_id AS role_id,
            u.email AS email,
            NULL AS aircraft
        FROM 
            roles AS r
        INNER JOIN 
            user_roles AS ur 
        ON 
            r.role_id = ur.role_id
        INNER JOIN 
            users AS u 
        ON 
            u.user_id = ur.user_id
        WHERE 
            r.role = roleName
            
        UNION
        
        SELECT 
            u.user_id AS user_id,
            r.role_id AS role_id,
            u.email AS email,
            NULL AS aircraft
        FROM 
            roles AS r
        INNER JOIN 
            user_roles AS ur 
        ON 
            r.role_id = ur.role_id
        INNER JOIN 
            users AS u 
        ON 
            u.user_id = ur.user_id
        WHERE 
            u.email = memberEmail
            
        UNION
         
        SELECT
            u.user_id AS user_id,
            NULL AS role_id,
            u.email AS email,
            a.name AS aircraft      
        FROM 
            aircrafts AS a
        INNER JOIN 
            aircraft_crew AS ac
        ON 
            a.aircraft_id = ac.aircraft_id    
        INNER JOIN
            users AS u 
        ON 
            u.user_id = ac.user_id
        WHERE 
            a.name = aircraftName
    ) AS combined_results
    GROUP BY email, user_id;
END //

DELIMITER ;
