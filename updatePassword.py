import mysql.connector

# Endpoint: profile/resetpassword
def update_password(body):
    connection = None
    cur = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="adsats_database"
        )
        
        print('Database connected correctly')
        
        email = body["email"]
        reset_password = body["reset_password"]
        
        # Create cursor
        cur = connection.cursor()
        
        sql_statement_1 = """UPDATE members
                             SET password = %s
                             WHERE email = %s"""
        
        cur.execute(sql_statement_1, (reset_password, email))
        
         # Commit the changes to the database
        connection.commit() 
        
        return {"status": "success", "message": "Password updated successfully"}
         
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"status": "error", "message": str(err)}
    
    finally: 
        if cur is not None:
            cur.close()
        if connection is not None:
            connection.close()
            
response = update_password({
    "user": "user",
    "email": "Shima@yahoo.com",
    "reset_password": "12301230"
})

print('Response:', response)
