import mysql.connector

def Delete_DocProc(body):
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        print("Database connected successfully")

        # Extract user input
        document_name = body.get("document_name")
        
        # Create a cursor object
        cursor = connection.cursor(buffered=True)

        # Call the stored procedure
        cursor.callproc("Delete_DocumentPROC", [document_name])
        
        # Commit the transaction
        connection.commit()

        return "Document deleted successfully"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Sample input to the function
response = Delete_DocProc({
    "document_name": "Purchase Order #91011.pdf"
})
print('Response:', response)
