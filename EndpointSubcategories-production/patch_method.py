from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update subcategory records based on the provided body.

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
        subcategory_id = body["subcategory_id"]
        # Update category fields if present in body
        if "subcategory_name" in body:
            update_subcategory_name(cursor, body["subcategory_name"], subcategory_id)
        if "archived" in body:
            update_archived(cursor, body["archived"], subcategory_id)
        if "description" in body:
            update_description(cursor, body["description"], subcategory_id)
        if "category_id" in body:
            update_category_id(cursor, body["category_id"], subcategory_id)
        # Commit the transaction
        connection.commit()
        return_body = {"category_id": subcategory_id}
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
def update_subcategory_name(
    cursor: MySQLCursorAbstract, subcategory_name: str, subcategory_id: int
) -> None:
    """
    Updates the subcategory name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        category_name (str): The new category name.
        subcategory_id (int): The ID of the subcategory to update.
    """
    update_query = """
        UPDATE subcategories
        SET subcategory_name = %s
        WHERE subcategory_id = %s
    """
    params = [subcategory_name, subcategory_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_archived(
    cursor: MySQLCursorAbstract, archived: int, subcategory_id: int
) -> None:
    """
    Updates the archived status of the subcategory.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        archived (int): The new archived status (1 for archived, 0 for not archived).
        subcategory_id (int): The ID of the subcategory to update.
    """
    update_query = """
        UPDATE subcategories
        SET archived = %s
        WHERE subcategory_id = %s
    """
    params = [archived, subcategory_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    subcategory_id: int,
) -> None:
    """
    Updates the description of the subcategory.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        description (str): The new description.
        subcategory_id (int): The ID of the subcategory to update.
    """
    update_query = """
        UPDATE subcategories
        SET description = %s
        WHERE subcategory_id = %s
    """
    params = [description, subcategory_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_category_id(
    cursor: MySQLCursorAbstract,
    category_id: int,
    subcategory_id: int,
) -> None:
    """ """
    update_query = """
        UPDATE subcategories
        SET category_id = %s
        WHERE subcategory_id = %s
    """
    params = [category_id, subcategory_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


# ===============================================================================
