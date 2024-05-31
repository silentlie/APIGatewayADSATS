import mysql.connector

# Endpoint: adsats/updatesubcategory
def Update_Subcategory(body):
    connection = None
    cur = None
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        print("Database connected correctly")
        
        user = body["user"]
        old_sub_name = body["old_sub_name"]
        new_sub_name = body["new_sub_name"]
       
        print("Processing request for user", user)
        
        # Create a cursor
        cur = connection.cursor()

        # Select subcategory_id for the old subcategory name
        select_subcategoryID_statement = """
            SELECT subcategory_id
            FROM subcategories
            WHERE name = %s
        """
        cur.execute(select_subcategoryID_statement, (old_sub_name,))
        subcategory_ID = cur.fetchone()
        
        if subcategory_ID:
            subcategory_ID = subcategory_ID[0]
            
            # Update subcategory name
            update_subcategory_statement = """
                UPDATE subcategories
                SET name = %s
                WHERE subcategory_id = %s
            """
            cur.execute(update_subcategory_statement, (new_sub_name, subcategory_ID))
            connection.commit()
            print("Subcategory name updated successfully")
        
        else:
            print("Subcategory not found")
            return "Subcategory not found"
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Error: {err}"

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')
    
    return "Success"

# Sample input to the function
response = Update_Subcategory({
    "user": "user",   
    "old_sub_name": "Double New Audit Program",
    "new_sub_name": "Audit_Program_1"
})
print('Response:', response)
