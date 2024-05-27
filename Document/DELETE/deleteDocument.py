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
            database="new_adsats_database"
        )
        
        print("Database connected correctly")
        
        user = body["user"]
        document_name = body.get("document_name")

        print("Processing request for user", user)

        # Create a cursor
        cur = connection.cursor()
        
        # Select the name of the documents
        selectdocument_statement = """
            SELECT document_id 
            FROM documents 
            WHERE file_name = %s
        """
        cur.execute(selectdocument_statement, (document_name,))
        docid_result = cur.fetchall()
        
        print("Documents found:", len(docid_result))
        
        for id in docid_result:
            print("Processing document ID:", id[0])

            # Delete from aircraft_documents -> Forignkey document_id
            aircraftdocument_forignkey_statement = """
                DELETE FROM aircraft_documents
                WHERE documents_id = %s
            """
            cur.execute(aircraftdocument_forignkey_statement, (id[0],))
            print('Deleted from aircraft_documents')

            # # Delete from documents_has_members -> Forignkey document_id
            # dochasmember_forignkey_statement = """
            #     DELETE FROM documents_has_members
            #     WHERE documents_id = %s
            # """
            # cur.execute(dochasmember_forignkey_statement, (id[0],))
            # print('Deleted from documents_has_members')

            # Delete from notice_documents -> Forignkey document_id
            notice_documents = """
                DELETE FROM notice_documents
                WHERE document_id = %s
            """
            cur.execute(notice_documents, (id[0],))
            print('Deleted from notice_documents')

            # Delete from documents -> parent
            document_statement = """
                DELETE FROM documents
                WHERE document_id = %s
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
    "document_name": "Aircraft Purchase Agreement.pdf"
})
print('Response:', response)
