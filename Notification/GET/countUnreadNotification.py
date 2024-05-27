import mysql.connector

# Endpoint: count_unread_notification
def CountUnreadNotification(body):
    try:
        connection = None
        cur = None
        
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        
        user = body["user"]
        status = body["status"]
        
        # create cursor
        cur = connection.cursor()
        
        # count unread notification
        countnotification_statement = """
            SELECT COUNT(*)
            FROM notifications
            WHERE status = %s    
        """
        
        cur.execute(countnotification_statement, (status,))
        result = cur.fetchone()
        unread_count = result[0] if result else 0
        
        return unread_count
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

response = CountUnreadNotification({
    "user": "user",
    "status": "unread"
})
print('Response:', response)
