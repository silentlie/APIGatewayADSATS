from helper import (
    connect_to_db,
    json_response,
    timer,
    Error,
    MySQLCursorAbstract
)

@timer
def patch_method(
    body: dict
) -> dict:
    """
    Patch method
    """
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        subcategory_id = body['subcategory_id']
        # Update name if present in body
        if 'subcategory_name' in body:
            update_subcategory_name(cursor,  body['subcategory_name'],subcategory_id)
        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], subcategory_id)
        # Update description value if present in body
        if 'description' in body:
            update_description(cursor, body['description'], subcategory_id)
        # Update category_id if present in body
        if 'category_id' in body:
            update_category_id(cursor, body['category_id'], subcategory_id)
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
def update_subcategory_name(
    cursor: MySQLCursorAbstract,
    subcategory_name: str,
    subcategory_id: int
) -> None:
    """
    Update name
    """
    update_query = """
        UPDATE subcategories
        SET subcategory_name = %s
        WHERE subcategory_id = %s
    """
    params = [subcategory_name, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_archived(
    cursor: MySQLCursorAbstract,
    archived: int,
    subcategory_id: int
) -> None:
    """
    Update archived or not
    """
    update_query = """
        UPDATE subcategories
        SET archived = %s
        WHERE subcategory_id = %s
    """
    params = [archived, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    subcategory_id: int,
) -> None:
    """
    Update description
    """
    update_query = """
        UPDATE subcategories
        SET description = %s
        WHERE subcategory_id = %s
    """
    params = [description, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_category_id(
    cursor: MySQLCursorAbstract,
    category_id: int,
    subcategory_id: int,
) -> None:
    """
    Update category_id
    """
    update_query = """
        UPDATE subcategories
        SET category_id = %s
        WHERE subcategory_id = %s
    """
    params = [category_id, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

#===============================================================================