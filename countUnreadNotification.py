import mysql.connector


#Endpointa:
def CountUnreadNotification(body):
    try:    
        connection = None
        cur = None
        
        connection = mysql.connector.connection(
            host = "localhost",
            username = "root",
            password = "",
            database = "adsats_database"
        )
        
        user = body["user"]
        status =body["status"]
        
        # create cursor
        cur = connection.cursor()
        
        # count unread notification
        # status in notification -> read/unread
        sql_statement = """
                        SELECT COUNT(status)
                        FROM notifications
                        WHERE status = %s    
                        """
        
        cur.execute(sql_statement,(status,))
     
    except mysql.connector.Error as err:
        print (f"Error : {err}")
        return None
    
    finally: 
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected:
            connection.close()
            print('Database connection closed')
            
response = CountUnreadNotification({
    "user": "user",
    "status": "unread"
   
})
print('Response:',response)

    
    