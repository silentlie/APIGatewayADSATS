CREATE PROCEDURE Delete_DocumentPROC(IN documentname VARCHAR(255))
BEGIN
    DECLARE docID INT DEFAULT 0;
    
    -- Select the document ID based on the document name
    SELECT document_id INTO docID
    FROM documents 
    WHERE name = documentname;

    -- Delete from aircraft_documents where document_id matches docID
    DELETE FROM aircraft_documents
    WHERE documents_id = docID;
    
    --  Delete from documents_has_members -> Forignkey document_id
    -- DELETE FROM documents_has_members
    -- WHERE documents_id = docID;
     
     -- Delete from notice_documents -> Forignkey document_id
     DELETE FROM notice_documents
     WHERE document_id = docID;
     
    --  Delete from documents -> parent
      DELETE FROM documents
      WHERE document_id = docID;
END