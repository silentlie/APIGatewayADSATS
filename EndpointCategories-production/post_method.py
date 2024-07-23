from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new category record.

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
        category_id = insert_category(cursor, body)

        # Commit the transaction to make the insert operation permanent
        connection.commit()

        # Prepare successful response
        return_body = {"category_id": category_id}
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
def insert_category(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new category record and returns the ID of the inserted record.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the fields for the new category.

    Returns:
        int: The ID of the newly inserted category.
    """
    query = """
    INSERT INTO categories (category_name, archived, created_at, description)
    VALUES (%s, %s, %s, %s)
    """
    params = [
        body["category_name"],
        body["archived"],
        body["created_at"],
        body["description"],
    ]
    cursor.execute(query, params)

    # Retrieve the last inserted ID
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict)
    category_id = result["id"]
    assert isinstance(category_id, int)

    print("Record inserted successfully with ID:", category_id)
    return category_id


################################################################################
