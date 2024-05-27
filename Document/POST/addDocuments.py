import mysql.connector
import datetime

# Endpoint: documents/adddocuments
def AddDocument(body):
    connection = None
    cur = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        print('Database connected correctly')
        
        user = body["user"]
        sub_name = body["sub_name"]
        member_email = body["member_email"]
        name_document = body["name_document"]
        archived = body["archived"]
        
        print("Processing request for user", user)
        
        # Create a cursor
        cur = connection.cursor()
        
        # Select subcategory
        subCategory_statement = """SELECT subcategory_id 
                                   FROM subcategories
                                   WHERE name = %s"""
        
        cur.execute(subCategory_statement, (sub_name,))
        sub_result = cur.fetchone()
        
        if sub_result:
            sub_id = sub_result[0]
            print("Subcategory ID:", sub_id) 
        else:
            print("Subcategory not found")
            return
        
        # Select member user_id (for uploaded_by_id)
        # For Insert -> person login can add new document
        loggedInUserID_statement = """SELECT user_id 
                              FROM users 
                              WHERE email = %s"""
                            
        cur.execute(loggedInUserID_statement, (member_email,))
        user_result = cur.fetchone()
    
        if user_result:
            member_id = user_result[0] 
            print("Logged-in User ID:", member_id) 
        else:
            print("User not found")
            return

        
        # uploded_by_id = user_id
        uplodedUserID_statement = """SELECT user_id 
                                      FROM users 
                                      WHERE email = %s"""
                            
        cur.execute(uplodedUserID_statement, (member_email,))
        uplodedUserID_result = cur.fetchone()
    
        if uplodedUserID_result:
            uplodedUser_id = uplodedUserID_result[0]
            print("uplodedUser_id :", uplodedUser_id)
        else:
            print("uplodedUser_id not found")
            return
        
        now = datetime.datetime.now()
        
        # Insert new document
        addDocument_statement = """INSERT INTO documents
                                   (subcategory_id,
                                    user_id,
                                    uploaded_by_id,
                                    created_at,
                                    modified_at,
                                    deleted_at,
                                    archived,
                                    file_name) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cur.execute(addDocument_statement, (sub_id, uplodedUser_id, member_id, now, now, None, archived, name_document))
        connection.commit()
        print("Document added successfully")
        return "Document added successfully"
        
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

response = AddDocument({
    "user": "user",
    "sub_name": "Aircraft manuals",
    "member_email": 'poxenham0@huffingtonpost.com',
    "name_document": "NEW Crew Training Program.pdf",
    "archived": 0
})
print('Response:', response)
