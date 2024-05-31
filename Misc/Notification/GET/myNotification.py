import mysql.connector

def MyNotification(body):
    connection = None
    cur = None
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        
        email = body["email"]
        limit = body["limit"]
        page = body["page"]
        
        offset = (page - 1) * limit
        
        cur = connection.cursor()
        
        sql_statement_1 = """
            SELECT n.deadline_at, n.subject, nf.read_at, nf.status
            FROM
                notices AS n
            INNER JOIN 
                notifications AS nf 
            ON 
                n.notice_id = nf.notice_id
            INNER JOIN 
                users AS u 
            ON 
                nf.user_id = u.user_id
            WHERE u.email = %s
            
            LIMIT %s OFFSET %s
        """
        
        cur.execute(sql_statement_1, (email, limit, offset))
        notices_result = cur.fetchall()
        
        if notices_result:
            for record in notices_result:
                print(record)
        else:
            print(None)
            
        return notices_result
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

response = MyNotification({
    "user": "user",
    "email": "amckeran2@instagram.com",
    "limit": 2,
    "page": 1
})
print('Response:', response)