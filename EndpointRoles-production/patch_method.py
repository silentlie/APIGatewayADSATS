from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update role records based on the provided body.

    Args:
        body (dict): The request body containing the fields to be updated.

    Returns:
        dict: The HTTP response dictionary with status code, headers, and body.
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500
    try:
        # Establish database connection
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        # Ensure role_id is in body
        if "role_id" not in body:
            raise ValueError("role_id is required")

        role_id = body["role_id"]

        # Update role fields if present in body
        if "role_name" in body:
            update_role_name(cursor, body["role_name"], role_id)
        if "archived" in body:
            update_archived(cursor, body["archived"], role_id)
        if "description" in body:
            update_description(cursor, body["description"], role_id)

        # Commit the transaction
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
def update_role_name(cursor: MySQLCursorAbstract, role_name: str, role_id: int) -> None:
    """
    Updates the role name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        role_name (str): The new role name.
        role_id (int): The ID of the role to update.
    """
    update_query = """
        UPDATE roles
        SET role_name = %s
        WHERE role_id = %s
    """
    params = [role_name, role_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_archived(cursor: MySQLCursorAbstract, archived: int, role_id: int) -> None:
    """
    Updates the archived status of the role.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        archived (int): The new archived status (1 for archived, 0 for not archived).
        role_id (int): The ID of the role to update.
    """
    update_query = """
        UPDATE roles
        SET archived = %s
        WHERE role_id = %s
    """
    params = [archived, role_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    role_id: int,
) -> None:
    """
    Updates the description of the role.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        description (str): The new description.
        role_id (int): The ID of the role to update.
    """
    update_query = """
        UPDATE roles
        SET description = %s
        WHERE role_id = %s
    """
    params = [description, role_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


################################################################################
