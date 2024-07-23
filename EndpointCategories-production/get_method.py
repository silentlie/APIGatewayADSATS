from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def get_method(parameters: dict) -> dict:
    """
    Handles GET requests to fetch category records based on various query parameters.

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

        if "limit" in parameters and "offset" in parameters:
            query, params = build_query(parameters)
            return_body = {
                "total_records": total_records(cursor, query, params),
                "categories": fetch_categories(cursor, query, params, parameters),
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
    Builds the SQL query and parameters for fetching category records.

    Args:
        parameters (dict): The query parameters for filtering the records.

    Returns:
        tuple: The SQL query string and list of parameters.
    """
    query = """
    SELECT
        *
    FROM categories
    """
    filters = []
    params = []

    # Add filters based on parameters
    if "search" in parameters:
        filters.append("category_name LIKE %s")
        params.append(f"%{parameters['search']}%")
    if "archived" in parameters:
        filters.append("archived = %s")
        params.append(parameters["archived"])
    if "created_at" in parameters:
        created_at_str = parameters["created_at"]
        assert isinstance(created_at_str, str), "created_at_str is not a str"
        created_at = created_at_str.split(",")
        filters.append("created_at BETWEEN %s AND %s")
        params.extend(created_at)

    # Append filters to the query
    if filters:
        query += " WHERE " + " AND ".join(filters)

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
    total_query = f"""
    SELECT
        COUNT(*) AS total_records
    FROM ({query}) AS initial_query
    """
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    assert isinstance(result, dict)
    total_records = result["total_records"]
    assert isinstance(total_records, int)
    return total_records


@timer
def fetch_categories(
    cursor: MySQLCursorAbstract, query: str, params: list, parameters: dict
) -> list:
    """
    Fetches category records with pagination and sorting.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        query (str): The SQL query string.
        params (list): The list of query parameters.
        parameters (dict): The query parameters for pagination and sorting.

    Returns:
        list: The list of category records.
    """
    # Add sorting if specified
    valid_columns = [
        "category_id",
        "category_name",
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
        query += f" ORDER BY {parameters['sort_column']} {parameters['order']}"

    # Add pagination
    query += " LIMIT %s OFFSET %s"
    params.append(int(parameters["limit"]))
    params.append(int(parameters["offset"]))

    cursor.execute(query, params)
    return cursor.fetchall()


################################################################################
