import mysql.connector
import datetime

# Endpoint: document/update_document
def UpdateDocument(body):
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
        
        email_login = body["email_login"]  
        document_name = body["document_name"]
        sub_category_name = body["sub_category_name"]
        new_document_name = body["new_document_name"]
        
        # Create a cursor
        cur = connection.cursor()
        
        # Extract id of document
        docID_statement = """SELECT 
                                document_id,
                                uploaded_by_id, 
                                archived,
                                subcategory_id 
                            FROM 
                                documents 
                            WHERE file_name = %s"""
        cur.execute(docID_statement, (document_name,))
        details_doc_result = cur.fetchone()  
        
        if details_doc_result:
            document_id = details_doc_result[0]
            uploaded_by_id = details_doc_result[1]
            archived = details_doc_result[2]
            subcategory_id = details_doc_result[3]
            print("Document ID:", document_id)
            print("Uploaded by ID:", uploaded_by_id)
            print("Archived:", archived)
            print("Subcategory ID:", subcategory_id)

        else:
            print("Document not found")
            return

        # Extract user_id from users, person login
        userID_statement = "SELECT user_id FROM users WHERE email = %s"
        cur.execute(userID_statement, (email_login,))
        userID = cur.fetchone() 

        if userID:
            # Unpack the tuple
            member = userID[0] 
            print("ID CurrentMember:", member)
        else:
            print("User not found")
            return
            
        # Compare and update user (between first user and person updating the document) 
        if uploaded_by_id == userID[0]:
            print("No need to change user")
            new_member_id = userID[0]
        else:
            new_member_id = userID[0]   
        
        # Extract subcategory
        subID_statement = """SELECT
                                subcategory_id,
                                categories_id 
                            FROM 
                                subcategories 
                            WHERE name = %s"""
        cur.execute(subID_statement, (sub_category_name,))
        id_subCategory = cur.fetchone()
        
        if id_subCategory:
            # Unpack the tuple
            id_subcategory, id_category = id_subCategory  
            print("Subcategory ID:", id_subcategory)
            print("Category ID:", id_category)       
        else:
            print("Subcategory not found")
            return
        
        # Compare and update subcategory 
        if subcategory_id == id_subcategory:
            print("No need to change subcategory")
            newSub_id = id_subcategory
        else:
            newSub_id = id_subcategory 
                 
        # Update documents Table 
        document_statement = """
            UPDATE documents
            SET 
                user_id = %s,
                file_name = %s,
                subcategory_id = %s,
                modified_at = %s
            WHERE document_id = %s
        """
        modified_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        cur.execute(document_statement, (new_member_id, new_document_name, newSub_id, modified_at, document_id))
        connection.commit()
        print('Document updated successfully')
        return 'Document updated successfully'
 
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

response = UpdateDocument({
    "email_login": "amckeran2@instagram.com",
    "document_name": "Purchase Order #272829.pdf",
    "sub_category_name": "Aircraft manuals",
    "new_document_name": "new_doc_3"
})

print('Response:', response)
