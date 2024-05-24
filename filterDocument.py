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
        filterDoc_statement = """"""
        cur.execute(filterDoc_statement, (documentName,))
        document_data = cur.fetchone()  # Fetch the result
        
       

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
