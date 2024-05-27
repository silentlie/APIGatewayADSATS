import mysql.connector
import datetime

# Endpoint: notice/insertnewnotice
def save_notice(body):
    connection = None
    cursor = None

    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        print("Database connected correctly")
        
        # Extract data from the request body
       
        email = body.get("email").strip().lower() 
        subject = body["subject"]
        category = body["category"]
        resolved = body["resolved"]
        time = body["time"]
        
        cursor = connection.cursor()
        
        # Print the email being queried
        print(f"Querying for email: {email}")
        
        # Get the member ID based on the provided email
        membersID_statement = "SELECT user_id FROM users WHERE TRIM(LOWER(email)) = %s"
        cursor.execute(membersID_statement, (email,))
        member_result = cursor.fetchone()
        
        # Print the result of the query
        print(f"Member result: {member_result}")
        
        if not member_result:
            print("User not found")
            return "User not found"
        
        member_id = member_result[0]
        print(f"User ID: {member_id}")
        
        # Get the maximum ID from the notices table
        maxID_statement = "SELECT MAX(notice_id) FROM notices"
        cursor.execute(maxID_statement)
        max_id_result = cursor.fetchone()
        max_id = max_id_result[0] if max_id_result[0] is not None else 0
        print(f"Current Max ID: {max_id}")
        
        # Calculate the next report number
        report_number = max_id + 1
        print(f"Next Report Number: {report_number}")
        
        # Insert new notice
        insert_notice_query = """
            INSERT INTO notices 
                (notice_id, 
                 subject,
                 created_by_id, 
                 category, 
                 created_at, 
                 resolved)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_notice_query, (report_number, subject, member_id, category, time, resolved))
        
        # Commit the transaction
        connection.commit()
        print("Notice saved successfully.")
        return "Success"
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if connection:
            connection.rollback()
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print('Database connection closed')

# Example usage
response = save_notice({
   
    "email": "amckeran2@instagram.com",
    "subject": "SubjectEX2",
    "category": "HazardNotice",
    "time": datetime.datetime.now(),
    "resolved": 0
})
print('Response:', response)
