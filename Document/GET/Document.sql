DELIMITER //

CREATE PROCEDURE GetDocuments (
    IN p_category_name VARCHAR(255),
    IN p_aircraft_name VARCHAR(255),
    IN p_limit INT,
    IN p_offset INT,
    IN p_archived TINYINT
)
BEGIN
    IF p_category_name IS NOT NULL AND p_aircraft_name IS NULL THEN
        SELECT d.file_name AS name, 
               DATE_FORMAT(d.created_at, '%Y-%m-%d') AS created_at, 
               d.archived

        FROM categories AS c
        INNER JOIN subcategories AS s 
            ON c.category_id = s.category_id 
        INNER JOIN  documents AS d 
            ON d.subcategory_id = s.subcategory_id
        WHERE 
            c.name = p_category_name AND d.archived = p_archived
        ORDER BY 
            d.created_at DESC
        LIMIT 
            p_limit OFFSET p_offset;
    
    ELSEIF p_category_name IS NOT NULL AND p_aircraft_name IS NOT NULL THEN
        
        SELECT d.file_name AS name,
               DATE_FORMAT(d.created_at, '%Y-%m-%d') AS created_at, 
               d.archived
        FROM categories AS c
        INNER JOIN subcategories AS s 
            ON c.category_id = s.category_id
        INNER JOIN documents AS d 
            ON d.subcategory_id = s.subcategory_id
        INNER JOIN aircraft_documents AS ad 
            ON ad.documents_id = d.document_id
        INNER JOIN aircrafts AS a 
            ON a.aircraft_id = ad.aircrafts_id
        WHERE 
            c.name = p_category_name    
                AND 
            a.name = p_aircraft_name
                 AND 
            d.archived = p_archived
        ORDER BY 
            d.created_at DESC
        LIMIT 
            p_limit OFFSET p_offset;
    
    ELSEIF p_category_name IS NULL AND p_aircraft_name IS NOT NULL THEN
       
        SELECT d.file_name AS name,
               DATE_FORMAT(d.created_at, '%Y-%m-%d') AS created_at, 
               d.archived
        FROM aircrafts AS a
        INNER JOIN aircraft_documents AS ad 
            ON a.aircraft_id = ad.aircrafts_id
        INNER JOIN documents AS d
            ON d.document_id = ad.documents_id
        WHERE 
            a.name = p_aircraft_name AND d.archived = p_archived
        ORDER BY 
            d.created_at DESC
        LIMIT 
            p_limit OFFSET p_offset;

    ELSEIF p_category_name IS NULL AND p_aircraft_name IS NULL THEN
       
        SELECT file_name, 
               DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, 
               archived
        FROM documents
        WHERE 
            archived = p_archived
        ORDER BY 
            created_at DESC
        LIMIT 
            p_limit OFFSET p_offset;
        
    END IF;
END //

DELIMITER ;
