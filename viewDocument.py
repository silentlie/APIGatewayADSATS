import mysql.connector

# Endpoint: document/view_document
def ViewDocument(body):
    connection = None
    cur = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",
            database="adsats_database"
        )
        print("Database connected correctly")

        documentName = body["documentName"]

        # Create a cursor
        cur = connection.cursor()
        
        # Extract document information
        viewDoc_statement = """SELECT members_id, subcategory_id, created_at, modified_at, name, type FROM documents WHERE name = %s"""
        cur.execute(viewDoc_statement, (documentName,))
        document_data = cur.fetchone()  # Fetch the result
        
        if document_data:
            # Print or process the fetched data
            members_id, subcategory_id, created_at, modified_at, name, type = document_data
            print("Members ID:", members_id)
            print("Subcategory ID:", subcategory_id)
            print("Created At:", created_at)
            print("Modified At:", modified_at)
            print("Name:", name)
            print("Type:", type)
        else:
            print("Document not found")

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

response = ViewDocument({
    "documentName": "doc4"
})
print('Response:', response)
