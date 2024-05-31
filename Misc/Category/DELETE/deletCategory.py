import mysql.connector

#I have problem with delete and update because we need to delete and update all of forign key in 
# other table ????????
# Function to delete a category
def delete_category(body):
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

        # Select categoryID
        select_categoryID = """ SELECT category_id
                                FROM categories
                                WHERE name = %s
                            """
        cur.execute(select_categoryID, (category_name,))
        category_id = cur.fetchone()

        if category_id:
            category_id = category_id[0]
            print(f"Category ID for '{category_name}': {category_id}")

            # Select subcategory_ids -> foreign key: documents
            select_subcategoryIDs = """SELECT subcategory_id
                                       FROM subcategories
                                       WHERE category_id = %s
                                    """
            cur.execute(select_subcategoryIDs, (category_id,))
            subcategory_ids = cur.fetchall()
            print("Subcategory IDs selected")

            if subcategory_ids:
                subcategory_ids = [subcat[0] for subcat in subcategory_ids]

                # Delete related rows from documents
                for subcat_id in subcategory_ids:
                    delete_documents = """ DELETE FROM documents
                                           WHERE subcategory_id = %s
                                       """
                    cur.execute(delete_documents, (subcat_id,))
                connection.commit()
                print("Related rows deleted from documents")

            # Delete from subcategories -> Foreign-key category
            foreignkey_delete_category = """ DELETE FROM subcategories
                                             WHERE category_id = %s
                                         """
            cur.execute(foreignkey_delete_category, (category_id,))
            connection.commit()
            print("Category ID deleted from subcategories")

            # Delete from categories
            delete_category = """DELETE FROM 
                                  categories 
                                  WHERE category_id = %s"""
            cur.execute(delete_category, (category_id,))
            connection.commit()
            print("Category deleted successfully")
        else:
            print("Category does not exist")

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
response = delete_category({
    "user": "user",
    "category_name": "aircraft",
})
print('Response:', response)
