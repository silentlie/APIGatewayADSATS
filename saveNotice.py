import mysql.connector
import datetime

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
        
       
        
        # Check if the report_number exists
        report_number_query = "SELECT id FROM notices WHERE id = %s"
        cursor.execute(report_number_query, (report_number,))
        report_result = cursor.fetchone()
        
        if report_result:
            # Update existing notice
            update_notice_query = """
                UPDATE notices
                SET subject = %s, category = %s, modified_at = %s, resolved = %s
                WHERE id = %s
            """
            cursor.execute(update_notice_query, (subject, category, time, resolved, report_number))
            # Commit the transaction
            connection.commit()
            print("Notice update successfully.")
            
        else:
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
