DELIMITER //

CREATE PROCEDURE Document(IN category_name VARCHAR(255), IN aircraft_name VARCHAR(255))
BEGIN
    IF category_name IS NULL AND aircraft_name IS NOT NULL THEN
        SELECT 
            a.id 
        FROM    
            aircrafts AS a
        INNER JOIN
            aircrafts_links AS al
        ON  
            a.id = al.aircrafts_id
        INNER JOIN
            documents AS d 
        ON 
            d.id = al.documents_id
        WHERE 
            a.name = aircraft_name;


    ELSE IF aircraft_name IS NULL AND category_name IS NOT NULL THEN
        SELECT 
            d.name
        FROM 
            categories As c
        INNER JOIN 
            subcategories s 
        ON  
            c.id = s.categories_id 
        INNER JOIN 
            documents AS d 
        ON  
            d.subcategory_id = s.subcategory_id
        WHERE  
            c.name = category_name;


    ELSE      
        SELECT 
            c.name AS category_name, 
            d.created_at AS document_date,
            a.name AS aircraft_name
        FROM 
            categories c
        INNER JOIN 
            subcategories s 
        ON 
            c.id = s.categories_id
        INNER JOIN 
            documents d
        ON
            d.id = s.subcategory_id
        INNER JOIN 
            aircrafts_links al
        ON 
            al.documents_id = d.id
        INNER JOIN
            aircrafts a
        ON
            a.id = al.aircrafts_id
        WHERE 
            c.name = category_name AND a.name = aircraft_name;

    END IF;
END //

DELIMITER ;
