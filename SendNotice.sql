DELIMITER //

CREATE PROCEDURE SendNotice(IN memberEmail VARCHAR(255), IN aircraftName VARCHAR(255), IN roleName VARCHAR(255))
BEGIN
    SELECT email, members_id 
    FROM (
        SELECT 
            m.id AS members_id,
            r.id AS rolesID,
            m.email AS email,
            NULL AS aircraft
        FROM 
            roles AS r
        INNER JOIN 
            members_has_roles AS mhr ON r.id = mhr.roles_id
        INNER JOIN 
            members AS m ON m.id = mhr.members_id
        WHERE 
            r.role = roleName
        
        UNION
        
        SELECT 
            m.id AS members_id,
            r.id AS rolesID,
            m.email AS email,
            NULL AS aircraft
        FROM 
            roles AS r
        INNER JOIN 
            members_has_roles AS mhr ON r.id = mhr.roles_id
        INNER JOIN 
            members AS m ON m.id = mhr.members_id
        WHERE 
            m.email = memberEmail
        
        UNION 
        
        SELECT
            m.id AS members_id,
            NULL AS rolesID,
            m.email AS email,
            a.name AS aircraft
        FROM 
            aircrafts AS a
        INNER JOIN 
            aircrafts_has_members AS ahm ON a.id = ahm.aircrafts_id
        INNER JOIN
            members AS m ON m.id = ahm.members_id
        WHERE 
            a.name = aircraftName
    ) AS combined_results
    GROUP BY email, members_id;
END //

DELIMITER ;
