from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new subcategory record.

    Args:
        body (dict): The request body containing the fields for the new category.

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
        # Insert the new category and get the ID
        subcategory_id = insert_subcategory(cursor, body)
        # Commit the transaction to make the insert operation permanent
        connection.commit()
        # Prepare successful response
        return_body = {"subcategory_id": subcategory_id}
        status_code = 201
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
def insert_subcategory(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new subcategory record and returns the ID of the inserted record.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the fields for the new subcategory.

    Returns:
        int: The ID of the newly inserted subcategory.
    """
    query = """
    INSERT INTO subcategories (subcategory_name, archived, created_at, description, category_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = [
        body["subcategory_name"],
        body["archived"],
        body["created_at"],
        body["description"],
        body["category_id"],
    ]
    cursor.execute(query, params)
    # Retrieve the last inserted ID
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict)
    subcategory_id = result["id"]
    assert isinstance(subcategory_id, int)
    print("Record inserted successfully with ID:", subcategory_id)
    return subcategory_id


# ===============================================================================
