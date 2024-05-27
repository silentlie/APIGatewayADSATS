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
            database="new_adsats_database"
        )
        print("Database connected correctly")

        document_name = body["document_name"]

        # Create a cursor
        cur = connection.cursor()

        # Extract document information
        viewDoc_statement = """ 
            SELECT 
                CONCAT(u.f_name, ' ', u.l_name) AS full_name,
                d.subcategory_id, 
                 d.created_at,
                d.modified_at,
                d.file_name, 
                d.archived 
            FROM
                documents AS d
            INNER JOIN 
                users AS u 
            ON  
                u.user_id = d.user_id
            WHERE d.file_name = %s
        """
        cur.execute(viewDoc_statement, (document_name,))
        document_data = cur.fetchall()  # Fetch the result

        if document_data:
            for doc in document_data:
                print(doc)
            return document_data
        else:
            print("Document not found")
            return None

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
    "document_name": "Crew Training Program Evaluation.pdf"
})
print('Response:', response)
