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
            database="adsats_database"
            )
        
        user = body["user"]
        email = body["email"]
    #create a cursor
        cur = connection.cursor()
        
        #use members , notices 
        # all notices that have been created by person login
        sql_statement_1 = """SELECT n.deadline_at,n.subject,nf.read_at,nf.status
                             FROM notices AS n 
                             INNER JOIN members AS m 
                             ON n.members_id = m.id
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
    "email":"Shima@yahoo.com"
  
   
})
print('Response:',response)