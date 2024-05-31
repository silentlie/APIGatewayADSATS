import mysql.connector

#Endpoint :mynotification/managenotification/
def MyNotification(body) :
    
    connection = None
    cur = None
    try:
        
        connection = mysql.connector.connect(
            host ="localhost",
            username ="root" ,
            password ="" ,
            database="new_adsats_database"
            )
        
        user = body["user"]
        email = body["email"]
    #create a cursor
        cur = connection.cursor()
        
        #use members , notices 
        # all notices that have been created by person login
        sql_statement_1 = """SELECT n.deadline_at,n.subject
                             FROM notices AS n 
                             INNER JOIN users AS u 
                             ON n.created_by_id = u.user_id
                             WHERE email =%s"""
        
        cur.execute(sql_statement_1,(email,))
        notices_result = cur.fetchall()
        
        if notices_result:
            for record in notices_result:
                print(record)
        else :
            print(None)
    
            
    except mysql.connector.Error as err:
        print (f"Error : {err}")
        return None
    
    finally: 
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected:
            connection.close()
            print('Database connection closed')
            
response = MyNotification({
    "user": "user",
    "email":"amckeran2@instagram.com"
  
   
})
print('Response:',response)