from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new role record and optionally link staff records.

    Args:
        body (dict): The request body containing the role details and optional staff IDs.

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

        # Insert the new role record and get the ID
        role_id = insert_role(cursor, body)

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
def insert_role(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new role record into the database.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the role details.

    Returns:
        int: The ID of the newly inserted role record.
    """
    query = """
    INSERT INTO roles (
        role_name,
        archived,
        created_at,
        description
    )
    VALUES (%s, %s, %s, %s)
    """
    params = [
        body["role_name"],
        body["archived"],
        body["created_at"],
        body["description"],
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict), "Result must be a dict"
    role_id = result["id"]
    assert isinstance(role_id, int), "role ID must be an integer"
    print("Record inserted successfully with ID:", role_id)
    return role_id


################################################################################
