import mysql.connector
import datetime

#endpoint :notice/insernewnotice
def save_notice(body):
    connection = None
    cursor = None

    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="adsats_database"
        )
        
        # Extract data from the request body
        username = body["username"]
        email = body["email"]
        subject = body["subject"]
        category = body["category"]
        resolved = body["resolved"]
        time = body["time"]
        
        cursor = connection.cursor()
        
        # Get the member ID based on the provided email
        membersID_statement ="SELECT id FROM members WHERE email = %s"
        cursor.execute(membersID_statement, (email,))
        member_result = cursor.fetchone()
        member_id = member_result[0]
        
        # Get the maximum ID from the notices table
        maxID_statement = "SELECT MAX(id) FROM notices"
        cursor.execute(maxID_statement ,)
        max_id_result = cursor.fetchone()
        max_id = max_id_result[0] 
        # Calculate the next report number
        report_number = max_id + 1
    
            # Insert new notice
        insert_notice_query = """
            INSERT INTO notices (id, subject, members_id, category, created_at, resolved)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_notice_query, (report_number, subject, member_id, category, time, resolved))
        # Commit the transaction
        connection.commit()
        print("Notice saved successfully.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print('Database connection closed')

# Example usage
response = save_notice({
    "username": "username",
    "email": "Sahar@yahoo.com",
    "subject": "SubjectEX2",
    "category": "HazardNotice",
    "time": datetime.datetime.now(),
    "resolved": 0
})
print('Response:', response)
