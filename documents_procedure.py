import mysql.connector

def Get_Document(body):
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
        category_name = body.get("category_name")
        aircraft_name = body.get("aircraft_name")
        
        # Create a cursor object
        cursor = connection.cursor(buffered=True)

        if category_name and aircraft_name:
            cursor.callproc('Document', [category_name, aircraft_name])
        elif category_name and not aircraft_name:
            cursor.callproc('Document', [category_name, None])
        elif aircraft_name and not category_name:
            cursor.callproc('Document', [None, aircraft_name])
        else:
            print("Either category_name or aircraft_name must be provided.")
            return None

        # Loop through the results from the stored procedure
        for result in cursor.stored_results():
            records = result.fetchall()
            print("Number of records:", len(records))
            for record in records:
                print(record)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Sample input to the function
response = Get_Document({
    "user": "user",  
    "category_name": "cat1",
    # "aircraft_name": "air1" 
})
print('Response:', response)
