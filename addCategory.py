import mysql.connector

# Function to Insert_New_Category
def Insert_New_Category(body):
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
        
        user = body["user"]
        category_name = body["category_name"]
        category_description = body["category_description"]
        print("Processing request for user", user)
        
        # Create a cursor
        cur = connection.cursor()
        
        # Add new category
        new_category = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        cur.execute(new_category, (category_name, category_description))
        
        # Commit the transaction
        connection.commit()
        
        print("Category added successfully")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

# Sample input to the function
response = Insert_New_Category({
    "user": "user",
    "category_name":"cate7",
    "category_description":"Specific category"
})
print('Response:', response)

   