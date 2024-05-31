import mysql.connector

# for deleteing we have to delete all of forginkeys ??? hva trouble
# Endpoint: adsats/deletesubcategory
def Delete_Subcategory(body):
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
        
        user = body["user"]
        sub_name = body["sub_name"]
       
        print("Processing request for user", user)
        
        # Create a cursor
        cur = connection.cursor()

        # Select sub_category
        select_subcategoryID_statement = """
            SELECT subcategory_id
            FROM subcategories
            WHERE name = %s
        """
        cur.execute(select_subcategoryID_statement, (sub_name,))
        subcategory_ID = cur.fetchone()
        
        if subcategory_ID:
            subcategory_ID = subcategory_ID[0]
            
            # Select document IDs associated with this subcategory
            select_documentid_statement = """
                SELECT document_id
                FROM documents
                WHERE subcategory_id = %s
            """
            cur.execute(select_documentid_statement, (subcategory_ID,))
            documents_result = cur.fetchall()
            
            if documents_result:
                for doc in documents_result:
                    doc_id = doc[0]
                    print(f"Document ID: {doc_id}")
                    
                    # Remove references from notice table
                    delete_notice_statement = """
                        DELETE FROM notice
                        WHERE document_id = %s
                    """
                    cur.execute(delete_notice_statement, (doc_id,))
                    
                    # Remove references from aircrafts table
                    delete_aircrafts_statement = """
                        DELETE FROM aircrafts
                        WHERE document_id = %s
                    """
                    cur.execute(delete_aircrafts_statement, (doc_id,))
                
                # Delete documents associated with this subcategory
                delete_document_statement = """
                    DELETE FROM documents
                    WHERE subcategory_id = %s
                """
                cur.execute(delete_document_statement, (subcategory_ID,))
            
            # Delete subcategory
            delete_subcategory_statement = """
                DELETE FROM subcategories
                WHERE subcategory_id = %s
            """
            cur.execute(delete_subcategory_statement, (subcategory_ID,))
            connection.commit()
            print("Subcategory and associated documents deleted successfully")
        
        else:
            print("Subcategory not found")
            return "Subcategory not found"
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Error: {err}"

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')
    
    return "Success"

# Sample input to the function
response = Delete_Subcategory({
    "user": "user",   
    "sub_name": "New Audit program",
})
print('Response:', response)
