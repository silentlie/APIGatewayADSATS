import mysql.connector
import datetime

#endpoint :notice/updatenewnotice
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
        
        # Extract data from the request body
        username = body["username"]
        email = body["email"]
        subject = body["subject"]
        category = body["category"]
        resolved = body["resolved"]
        current_time = body["current_time"]
        report_number = body["report_number"]
        
        cursor = connection.cursor()
        
        # Get the member ID based on the provided email
        membersID_statement ="SELECT user_id FROM users WHERE email = %s"
        cursor.execute(membersID_statement, (email,))
        member_result = cursor.fetchone()
        member_id = member_result[0]
        
        
       # Check if the report_number exists
        report_number_query = "SELECT notice_id FROM notices WHERE notice_id = %s"
        cursor.execute(report_number_query, (report_number,))
        report_result = cursor.fetchone()
        
        if report_result:
            # Update existing notice
            update_notice_query = """
                UPDATE notices
                SET subject = %s, 
                    category = %s, 
                    modified_at = %s, 
                    resolved = %s,
                    created_by_id = %s 
                WHERE notice_id = %s
            """
            cursor.execute(update_notice_query, (subject, category, current_time, resolved, member_id,report_number))
            # Commit the transaction
            connection.commit()
            print("Notice update successfully.")

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
    "email": "amckeran2@instagram.com",
    "subject": "NEW: Mold growth detected in the basemen..",
    "category": "Notice",
    "current_time": datetime.datetime.now(),
    "resolved": 0,
    "report_number" :2
})
print('Response:', response)
