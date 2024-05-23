import mysql.connector
import datetime
# make empty string for key,and insert to document table,
#
# Connection to the database
def fetch_subcategory_id(body):
    connection = None
    cur = None
    try:
        connection = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "adsats_database"
            )
        print ('Database Connect correctly')
        
    # Endpoint:documents/adddocuments
    # HTTP Method: POST
        user = body["user"]
        sub_name = body["sub_name"]
        member_email = ["member_email"]
        name_document = ["name_document"]
        print("procceesing request for user",user)
        
    #    
    
    # Create a cursor 
        cur = connection.cursor()
        
        # Select subcategory 
        sql_statement_1 = "SELECT subcategory_id FROM subcategories where name = %s"
        
        cur.execute(sql_statement_1,(sub_name ,))
        sub_result = cur.fetchall()
        
        if sub_result:
            sub_id = sub_result[0][0]
            print(sub_id) 
        else:
            print (None)
        
        #select user
        sql_statement_2 = "SELECT id FROM members where email = %s"
        cur.execute( sql_statement_2,(member_email,))
        user_result = cur.fetchall()
    
        if user_result:
            member_id = user_result[0][0] 
            print(member_id) 
        else:
            print(None)  
       
        now = datetime.datetime.now()
       #insert addnewdocument
        sql_statement_3 = "INSERT INTO documents(subcategory_id,members_id,created_at,modified_at,deleted_at,name) VALUES(%s,%s,%s,%s,%s,)"
        cur.execute(sql_statement_3,(sub_id,member_id,now,now,None,name_document,))
    except mysql.connector.Error as err:
        print(f"Error:{err}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')
    
    
resopnse = fetch_subcategory_id({
    "user": "user",
    "sub_name" : "sub1",
    "member_email" : 'Ali@yahoo.com',
    "name_document" : "newAddDocument"
})
print('Response:',resopnse)


   
