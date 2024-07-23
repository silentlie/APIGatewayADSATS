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
    connection = None
    cursor = None
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        role_id = body['role_id']
        # Update name if present in body
        if 'role_name' in body:
            update_role_name(cursor,  body['role_name'],role_id)
        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], role_id)
        # Update description value if present in body
        if 'description' in body:
            update_description(cursor, body['description'], role_id)
        connection.commit()
        return_body = {"role_id": role_id}
        status_code = 200
    except Error as e:
        # Handle SQL error
        return_body = {"error": e._full_msg}
        if e.errno == 1062:
            status_code = 409  # Conflict error
    except Exception as e:
        # Handle general error
        return_body = {"error": str(e)}
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    response = json_response(status_code, return_body)
    print(response)
    return response

@timer
def update_role_name(
    cursor: MySQLCursorAbstract,
    role_name: str,
    role_id: int
) -> None:
    """
    Update name
    """
    update_query = """
        UPDATE roles
        SET role_name = %s
        WHERE role_id = %s
    """
    params = [role_name, role_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_archived(
    cursor: MySQLCursorAbstract,
    archived: int,
    role_id: int
) -> None:
    """
    Update archived or not
    """
    update_query = """
        UPDATE roles
        SET archived = %s
        WHERE role_id = %s
    """
    params = [archived, role_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    role_id: int,
) -> None:
    """
    Update description
    """
    update_query = """
        UPDATE roles
        SET description = %s
        WHERE role_id = %s
    """
    params = [description, role_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

#===============================================================================