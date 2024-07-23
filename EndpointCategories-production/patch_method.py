from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update category records based on the provided body.

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
        category_id = body["category_id"]

        # Update category fields if present in body
        if "category_name" in body:
            update_category_name(cursor, body["category_name"], category_id)
        if "archived" in body:
            update_archived(cursor, body["archived"], category_id)
        if "description" in body:
            update_description(cursor, body["description"], category_id)

        # Commit the transaction
        connection.commit()
        return_body = {"category_id": category_id}
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
def update_category_name(
    cursor: MySQLCursorAbstract, category_name: str, category_id: int
) -> None:
    """
    Updates the category name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        category_name (str): The new category name.
        category_id (int): The ID of the category to update.
    """
    update_query = """
        UPDATE categories
        SET category_name = %s
        WHERE category_id = %s
    """
    params = (category_name, category_id)
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_archived(
    cursor: MySQLCursorAbstract, archived: int, category_id: int
) -> None:
    """
    Updates the archived status of the category.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        archived (int): The new archived status (1 for archived, 0 for not archived).
        category_id (int): The ID of the category to update.
    """
    update_query = """
        UPDATE categories
        SET archived = %s
        WHERE category_id = %s
    """
    params = (archived, category_id)
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


@timer
def update_description(
    cursor: MySQLCursorAbstract, description: str, category_id: int
) -> None:
    """
    Updates the description of the category.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        description (str): The new description.
        category_id (int): The ID of the category to update.
    """
    update_query = """
        UPDATE categories
        SET description = %s
        WHERE category_id = %s
    """
    params = (description, category_id)
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} records successfully updated")


################################################################################
