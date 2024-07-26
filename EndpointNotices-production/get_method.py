from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def get_method(parameters: dict) -> dict:
    """
    Handles GET requests to fetch notice records based on various query parameters.

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
                "notices": fetch_notices(cursor, query, params, parameters),
            }
        elif "notice_id" in parameters:
            notice_id = parameters["notice_id"]
            return_body = {
                "aircraft": specific_aircraft_notices(cursor, notice_id),
                "staff": specific_notices_staff(cursor, notice_id),
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
    Builds the SQL query and parameters for fetching notice records.

    Args:
        parameters (dict): The query parameters for filtering the records.

    Returns:
        tuple: The SQL query string and list of parameters.
    """
    query = """
    SELECT
        n.*
    FROM notices AS n
    JOIN notices_staff AS ns
    ON n.notice_id = ns.notice_id
    """
    filters = []
    params = []

    if "staff_id" not in parameters:
        raise ValueError("staff_id is required")
    staff_id = parameters["staff_id"]

    if "tab" in parameters:
        tab = parameters["tab"]
        if tab == "inbox":
            filters.append("n.staff_id = %s")
        elif tab == "sent":
            filters.append("ns.staff_id = %s")
        else:
            raise ValueError("Invalid tab value")
    else:
        raise ValueError("tab is required")

    params.append(staff_id)

    if "search" in parameters:
        filters.append("notice_name LIKE %s")
        params.append(f"%{parameters['search']}%")
    if "archived" in parameters:
        filters.append("archived = %s")
        params.append(parameters["archived"])
    if "created_at" in parameters:
        created_at = parameters["created_at"].split(",")
        filters.append("created_at BETWEEN %s AND %s")
        params.extend(created_at)

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
    total_query = f"SELECT COUNT(*) as total_records FROM ({query}) AS initial_query"
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    assert isinstance(result, dict)
    total_records = result["total_records"]
    assert isinstance(total_records, int)
    return total_records


@timer
def fetch_notices(
    cursor: MySQLCursorAbstract, query: str, params: list, parameters: dict
) -> list:
    """
    Fetches notice records with pagination and sorting.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        query (str): The SQL query string.
        params (list): The list of query parameters.
        parameters (dict): The query parameters for pagination and sorting.

    Returns:
        list: The list of notice records.
    """
    valid_columns = [
        "notice_id",
        "notice_name",
        "archived",
        "noticed_at",
        "deadline_at",
    ]
    valid_orders = ["ASC", "DESC"]

    if (
        "sort_column" in parameters
        and "order" in parameters
        and parameters["sort_column"] in valid_columns
        and parameters["order"] in valid_orders
    ):
        query += " ORDER BY %s %s"
        params.extend([parameters["sort_column"], parameters["order"]])

    query += " LIMIT %s OFFSET %s"
    params.extend([int(parameters["limit"]), int(parameters["offset"])])

    cursor.execute(query, params)
    return cursor.fetchall()


@timer
def specific_aircraft_notices(cursor: MySQLCursorAbstract, notice_id: int) -> list:
    """
    Returns a list of aircraft linked with a specific notice ID.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The notice ID to query.

    Returns:
        list: The list of aircraft IDs.
    """
    query = "SELECT aircraft_id FROM aircraft_notices WHERE notice_id = %s"
    cursor.execute(query, [notice_id])
    return cursor.fetchall()


@timer
def specific_notices_staff(cursor: MySQLCursorAbstract, notice_id: int) -> list:
    """
    Returns a list of staff linked with a specific notice ID.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The notice ID to query.

    Returns:
        list: The list of aircraft IDs.
    """
    query = "SELECT staff_id FROM notices_staff WHERE notice_id = %s"
    cursor.execute(query, [notice_id])
    return cursor.fetchall()


@timer
def specific_documents_notices(cursor: MySQLCursorAbstract, notice_id: int) -> list:
    """
    Returns a list of document linked with a specific notice ID.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The notice ID to query.

    Returns:
        list: The list of documents.
    """
    query = "SELECT document_name FROM documents_notices WHERE notice_id = %s"
    cursor.execute(query, [notice_id])
    return cursor.fetchall()

################################################################################
