from helper import (
    connect_to_db,
    json_response,
    timer,
    Error,
    MySQLCursorAbstract
)

@timer
def get_method(
    parameters: dict
) -> dict:
    """
    Handles GET requests to fetch subcategory records based on various query parameters.

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
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        if "limit" in parameters and "offset" in parameters:
            query, params = build_query(parameters)
            return_body = {
                "total_records": total_records(cursor, query, params),
                "categories": fetch_subcategories(cursor, query, params, parameters),
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
    return_body = json_response(status_code, return_body)
    print (return_body)
    return return_body

@timer
def build_query(
    parameters: dict
) -> tuple:
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
    FROM subcategories
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search for name
    if 'search' in parameters:
        filters.append("subcategory_name LIKE %s")
        params.append(parameters["search"])
    # filter based on archived or not
    if 'archived' in parameters:
        filters.append("archived = %s")
        params.append(parameters["archived"])
    # filter based on date range when it was added
    if 'created_at' in parameters:
        created_at = parameters["start_at"].split(',')
        filters.append("start_at BETWEEN %s AND %s")
        params.extend(created_at)
    # if there is any filter add to query
    if filters:
        query += "WHERE " + " AND ".join(filters)
    # finish prepare query and params
    return query, params

@timer
def total_records(
    cursor: MySQLCursorAbstract,
    query: str,
    params: list
) -> int:
    """
    Returns the total number of records matching the query.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        query (str): The SQL query string.
        params (list): The list of query parameters.

    Returns:
        int: The total number of records.
    """
    total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
    print(total_query)
    print(params)
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    assert isinstance(result, dict)
    total_records = result['total_records']
    assert isinstance(total_records, int)
    return total_records

@timer
def fetch_subcategories(
    cursor: MySQLCursorAbstract, query: str, params: list, parameters: dict
) -> list:
    """
    Returns the total number of records matching the query.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        query (str): The SQL query string.
        params (list): The list of query parameters.

    Returns:
        int: The total number of records.
    """
    # sort column if need it, default is pk
    valid_columns = [
        "subcategory_id",
        "subcategory_name",
        "archived",
        "created_at",
        "updated_at",
    ]
    valid_orders = [
        "ASC",
        "DESC"
    ]
    if (
        'sort_column' in parameters
        and 'order' in parameters
        and parameters['sort_column'] in valid_columns
        and parameters['order'] in valid_orders
    ):
        query += " ORDER BY %s %s"
        params.append(parameters['sort_column'])
        params.append(parameters['order'])
    # pagination
    query += " LIMIT %s OFFSET %s "
    params.append(int(parameters["limit"]))
    params.append(int(parameters["offset"]))
    # finish query
    print(query)
    print(params)
    cursor.execute(query, params)
    return cursor.fetchall()

#===============================================================================