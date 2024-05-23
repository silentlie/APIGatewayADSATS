import mysql.connector

# Function to Insert new sub_category
def Insert_new_Sub(body):
    connection = None
    cur = None
    category_id = None
    
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="adsats_database"
        )
        
        print("Database connected correctly")
        
        user = body["user"]
        category_name = body["category_name"]
        sub_name = body["sub_name"]
        print("Processing request for user", user)
        
        # Create a cursor
        cur = connection.cursor()
        
        # Select category_id
        select_category = "SELECT id FROM categories WHERE name = %s"
        cur.execute(select_category, (category_name,))
        result = cur.fetchone()
        
        # Print category id
        if result:
            category_id = result[0]
            print("Category ID:", category_id)
        else:
            print("Category not found")
            return None
        
        # Insert new sub_category
        add_subcategory = "INSERT INTO subcategories (name, categories_id) VALUES (%s, %s)"
        cur.execute(add_subcategory, (sub_name, category_id))
        
        # Commit the transaction
        connection.commit()
        
        print("Sub-category added successfully")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')
    
    return "Success"

# Sample input to the function
response = Insert_new_Sub({
    "user": "user",
    "category_name": "cate7",
    "sub_name": "sub-cate7"
})
print('Response:', response)
