import mysql.connector

#Endpoint: document/delete_document
def DeleteDocument(body):
    connection = None
    cur = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Corrected 'username' to 'user'
            password="",
            database="adsats_database"
        )
        
        print("Database connected correctly")
        
        user = body["user"]
        documentName = body.get("documentName")

        print("Processing request for user", user)

        # Create a cursor
        cur = connection.cursor()
        
        # Select the name of the documents
        selectdocument_statement = """
            SELECT id 
            FROM documents 
            WHERE name = %s
        """
        cur.execute(selectdocument_statement, (documentName,))
        docid_result = cur.fetchall()
        
        print("Documents found:", len(docid_result))
        
        for id in docid_result:
            print("Processing document ID:", id[0])

            # Delete from aircrafts_links -> Forignkey document_id
            aircraftslinks_forignkey_statement = """
                DELETE FROM aircrafts_links
                WHERE documents_id = %s
            """
            cur.execute(aircraftslinks_forignkey_statement, (id[0],))
            print('Deleted from aircrafts_links')

            # Delete from documents_has_members -> Forignkey document_id
            dochasmember_forignkey_statement = """
                DELETE FROM documents_has_members
                WHERE documents_id = %s
            """
            cur.execute(dochasmember_forignkey_statement, (id[0],))
            print('Deleted from documents_has_members')

            # Delete from notifications_has_documents -> Forignkey document_id
            notificationhasdoc_forignkey_statement = """
                DELETE FROM notifications_has_documents
                WHERE documents_id = %s
            """
            cur.execute(notificationhasdoc_forignkey_statement, (id[0],))
            print('Deleted from notifications_has_documents')

            # Delete from documents -> parent
            document_statement = """
                DELETE FROM documents
                WHERE id = %s
            """
            cur.execute(document_statement, (id[0],))
            print('Deleted from documents')
        
        # Commit the transaction
        connection.commit()
        print('Transaction committed')
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if connection:
            connection.rollback()
            print('Transaction rolled back due to error')
        return None
    
    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

response = DeleteDocument({
    "user": "user",
    "documentName": "doc1"
})
print('Response:', response)
