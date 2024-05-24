import mysql.connector
import datetime
# we donot have category and aircraft in document is need to update?????
# Endpoint: document/update_document
def DeleteDocument(body):
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
        
        
        # email = body["email"]  
        documentName = body["documentName"]
        subCategoryName = body["subCategoryName"]
        newDocumentName = body["newDocumentName"]
        
    
        # Create a cursor
        cur = connection.cursor()
        
        # Extract id of document
        docID_statement = """SELECT id, members_id, subcategory_id FROM documents WHERE name = %s"""
        cur.execute(docID_statement, (documentName,))
        id_doc = cur.fetchone()  
        
        if id_doc:
            # Unpack the tuple
            id_value, member_id_value, id_subcategory_value = id_doc  
            print("ID:", id_value)
            print("Member ID:", member_id_value)
            print("subcategory ID:", id_subcategory_value)
        else:
            print("Document not found")

        # # Extract member_id from members
        # memberID_statement = "SELECT id FROM members WHERE email = %s"
        # cur.execute(memberID_statement, (email,))
        # id_member = cur.fetchone() 

        # if id_member:
        #     # Unpack the tuple
        #     member = id_member[0] 
        #     print("ID CurrentMembers:", member)
            
        # #compare two members 
        # if member_id_value == id_member[0]:
        #     print ("No need to change")
        #     newmember_id = id_member[0]
        # else:
        #     newmember_id = id_member[0]   
        
        # Extract subcategory
        subID_statement = """SELECT subcategory_id,categories_id FROM subcategories WHERE name = %s"""
        cur.execute(subID_statement, (subCategoryName,))
        id_subCategory = cur.fetchone()
        
        
        if id_subCategory:
         # Unpack the tuple
            id_subcategory, id_category = id_subCategory  
            print("subID:", id_subcategory)
            print("catID:", id_category)       
        else:
            print("subcategory not found")
        
        # compare two members 
        if id_subcategory_value == id_subcategory:
            print ("No need to change")
            newSub_id = id_subcategory
        else:
           newSub_id = id_subcategory 
                 
        # Update documents Table 
        document_statement = """
            UPDATE documents
            SET 
                name = %s,
                subcategory_id = %s,
                modified_at = %s
            WHERE id = %s
            """
        modified_at = datetime.datetime.now().strftime('%Y-%m-%d')  
        cur.execute(document_statement, (newDocumentName,newSub_id, modified_at, id_value))
        connection.commit()
        print('Update from documents')
 
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
    # "email": "Shima@yahoo.com",
    "documentName": "doc3",
    "subCategoryName" :"sub3",
    "newDocumentName" :"newdoc3"
})
print('Response:', response)
