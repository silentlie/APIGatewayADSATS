CREATE PROCEDURE Delete_DocumentPROC(IN documentname VARCHAR(255))
BEGIN
    DECLARE docID INT DEFAULT 0;
    
    -- Select the document ID based on the document name
    SELECT id INTO docID
    FROM documents 
    WHERE name = documentname;

    -- Delete from aircrafts_links where document_id matches docID
    DELETE FROM aircrafts_links
    WHERE documents_id = docID;
    
    --  Delete from documents_has_members -> Forignkey document_id
     DELETE FROM documents_has_members
     WHERE documents_id = docID;
     
     -- Delete from notifications_has_documents -> Forignkey document_id
     DELETE FROM notifications_has_documents
     WHERE documents_id = docID;
     
      # Delete from documents -> parent
      DELETE FROM documents
      WHERE id = docID;
END