from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def get_method(parameters: dict) -> dict:
    """
    Handles GET requests to fetch staff records based on various query parameters.

    Args:
        parameters (dict): The query parameters for the request.

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

        if "staff_id" in parameters:
            staff_id = int(parameters["staff_id"])
            return_body = {
                "aircraft_ids": specific_aircraft_staff(cursor, staff_id),
                "role_ids": specific_role_staff(cursor, staff_id),
                "subcategory_ids": specific_staff_subcategories(cursor, staff_id),
            }
        elif "limit" in parameters and "offset" in parameters:
            query, params = build_query(parameters)
            return_body = {
                "total_records": total_records(cursor, query, params),
                "staff": staff(cursor, query, params, parameters),
            }
        else:
            raise ValueError("Invalid use of method")

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
def build_query(parameters: dict) -> tuple:
    """
    Builds the SQL query and parameters for fetching staff records.

    Args:
        parameters (dict): The query parameters for filtering the records.

    Returns:
        tuple: The SQL query string and list of parameters.
    """
    query = """
    SELECT
        *
    FROM staff
    """
    # Define filters if any
    filters = []
    # Parameters for binding
    params = []
    # Search for name
    if "search" in parameters:
        filters.append("staff_name LIKE %s")
        params.append(f"%{parameters['search']}%")
    # Filter based on archived or not
    if "archived" in parameters:
        filters.append("archived = %s")
        params.append(parameters["archived"])
    # Filter based on date range when it was added
    if "created_at" in parameters:
        created_at_str = parameters["created_at"]
        assert isinstance(created_at_str, str), "created_at_str is not a str"
        created_at = created_at_str.split(",")
        filters.append("created_at BETWEEN %s AND %s")
        params.extend(created_at)
    # If there are any filters, add them to the query
    if filters:
        query += " WHERE " + " AND ".join(filters)
    # Finish preparing query and params
    return query, params


@timer
def total_records(cursor: MySQLCursorAbstract, query: str, params: list) -> int:
    """
    Returns the total number of records matching the query.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        query (str): The SQL query string.
        params (list): The list of query parameters.

    Returns:
        int: The total number of records.
    """
    total_query = f"SELECT COUNT(*) as total_records FROM ({query}) AS initial_query"
    print(total_query)
    print(params)
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    assert isinstance(result, dict), "Result must be a dict"
    total_records = result["total_records"]
    assert isinstance(total_records, int), "Total records must be an integer"
    return total_records


@timer
def staff(
    cursor: MySQLCursorAbstract, query: str, params: list, parameters: dict
) -> list:
    """
    Fetches staff records with pagination and sorting.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        query (str): The SQL query string.
        params (list): The list of query parameters.
        parameters (dict): The query parameters for pagination and sorting.

    Returns:
        list: The list of staff records.
    """
    # Sort column if needed, default is pk
    valid_columns = [
        "staff_id",
        "staff_name",
        "archived",
        "created_at",
        "updated_at",
    ]
    valid_orders = ["ASC", "DESC"]
    if (
        "sort_column" in parameters
        and "order" in parameters
        and parameters["sort_column"] in valid_columns
        and parameters["order"] in valid_orders
    ):
        query += " ORDER BY %s %s"
        params.append(parameters["sort_column"])
        params.append(parameters["order"])
    # Pagination
    query += " LIMIT %s OFFSET %s"
    params.append(int(parameters["limit"]))
    params.append(int(parameters["offset"]))
    # Finish query
    cursor.execute(query, params)
    return cursor.fetchall()


@timer
def specific_aircraft_staff(cursor: MySQLCursorAbstract, staff_id: int) -> list:
    """
    Returns a list of aircraft linked with a specific staff ID.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The staff ID to query.

    Returns:
        list: The list of aircraft IDs.
    """
    query = """
        SELECT
            aircraft_id
        FROM aircraft_staff
        WHERE staff_id = %s
    """
    cursor.execute(query, [staff_id])
    return cursor.fetchall()


@timer
def specific_role_staff(cursor: MySQLCursorAbstract, staff_id: int) -> list:
    """
    Returns a list of roles linked with a specific staff ID.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The staff ID to query.

    Returns:
        list: The list of role IDs.
    """
    query = """
        SELECT
            role_id
        FROM roles_staff
        WHERE staff_id = %s
    """
    cursor.execute(query, [staff_id])
    return cursor.fetchall()


@timer
def specific_staff_subcategories(cursor: MySQLCursorAbstract, staff_id: int) -> list:
    """
    Returns a list of subcategories linked with a specific staff ID.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The staff ID to query.

    Returns:
        list: The list of subcategory IDs and access level IDs.
    """
    query = """
        SELECT
            subcategory_id,
            access_level_id
        FROM staff_subcategories
        WHERE staff_id = %s
    """
    cursor.execute(query, [staff_id])
    return cursor.fetchall()


################################################################################
