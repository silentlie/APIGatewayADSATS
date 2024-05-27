import mysql.connector

# Endpoint : document/adddocument/subcategory/addcategory
def Insert_New_Category(body):
    connection = None
    cur = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        print('Database connected correctly')
        
        user = body["user"]
        category_name = body["category_name"]
        
        print("Processing request for user", user)
        
        # Create a cursor
        cur = connection.cursor()
        
        # Add new category
        new_category = "INSERT INTO categories (name) VALUES (%s)"
        cur.execute(new_category, (category_name, ))
        
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
   
})
print('Response:', response)

   