from helper import (
    connect_to_db,
    json_response,
    timer,
    Error,
    MySQLCursorAbstract
)

@timer
def post_method(
    body: dict
) -> dict:
    """
    Post method
    """
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        # Insert the new record and get the id
        subcategory_id = insert_subcategory(cursor, body)
        # Commits the transaction to make the insert operation permanent
        # If any error is raised, there'll be no commit
        connection.commit()
        return_body = subcategory_id
        status_code = 200
    # Catch SQL exeption
    except Error as e:
        return_body = f"SQL Error: {e._full_msg}"
        # Error no 1062 means duplicate name
        if e.errno == 1062:
            # Code 409 means conflict in the state of the server
            status_code = 409
    # Catch other exeptions
    except Exception as e:
        return_body = f"SQL Error: {e}"
    # Close cursor and connection
    finally:
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    response = json_response(status_code, return_body)
    print (response)
    return response

@timer
def insert_subcategory(
    cursor: MySQLCursorAbstract,
    body: dict
) -> int:
    """
    Insert new record and return id
    """
    query = """
    INSERT INTO subcategories (subcategory_name, archived, created_at, description, category_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = [body["subcategory_name"], body["archived"], body["created_at"], body["description"], body["category_id"]]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID()")
    subcategory_id = cursor.fetchone()
    assert isinstance(subcategory_id, int)
    print("Record inserted successfully with ID:", subcategory_id)
    return subcategory_id

#===============================================================================