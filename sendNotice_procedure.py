import mysql.connector
#use Procedure for sending notice
def notice_procedure(body):
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="adsats_database"
        )
        print("Database connected successfully")

        # Extract user input
        member_emails = body.get("memberEmail", [])
        aircraft_names = body.get("aircraftName", [])
        role_names = body.get("roleName", [])

        # Create a cursor object
        cursor = connection.cursor(buffered=True)
        
        # Prepare the stored procedure call
        results = []
        for member_email in member_emails:
            for aircraft_name in aircraft_names:
                for role_name in role_names:
                    cursor.callproc('SendNotice', [member_email, aircraft_name, role_name])
                    
                    # Fetch results from all result sets
                    for result in cursor.stored_results():
                        results.extend(result.fetchall())

        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Sample input to the function
response = notice_procedure({
    "memberEmail": ["Shima@yahoo.com", "Sahar@yahoo.com"],
    "aircraftName": ["air1", "air2"],
    "roleName": ["role1"]
})
print('Response:', response)
