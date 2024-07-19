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
        category_id = body['category_id']
        
        # Update name if present in body
        if 'category name' in body:
            update_category_name(cursor,  body['category_name'],category_id)

        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], category_id)
        
        # Update description value if present in body
        if 'description' in body:
            update_description(cursor, body['description'], category_id)
        connection.commit()
        return_body = category_id
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
def update_category_name(
    cursor: MySQLCursorAbstract,
    category_name: str,
    category_id: int
) -> None:
    """
    Update name
    """
    update_query = """
        UPDATE categories
        SET category_name = %s
        WHERE category_id = %s
    """
    params = [category_name, category_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")


@timer
def update_archived(
    cursor: MySQLCursorAbstract,
    archived: int,
    category_id: int
) -> None:
    """
    Update archived or not
    """
    update_query = """
        UPDATE categories
        SET archived = %s
        WHERE category_id = %s
    """
    params = [archived, category_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    category_id: int
) -> None:
    """
    Update description
    """
    update_query = """
        UPDATE categories
        SET description = %s
        WHERE category_id = %s
    """
    params = [description, category_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

#===============================================================================