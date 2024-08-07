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

        if "staff_id" not in parameters:
            raise ValueError("staff_id is required")
        staff_id = parameters["staff_id"]
        return_body = fetch_notifications(cursor, staff_id)
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
def fetch_notifications(cursor: MySQLCursorAbstract, staff_id: int) -> list:
    """
    """
    query = """
    SELECT
        n.notice_id,
        n.subject,
        n.type,
        n.staff_id,
        n.notice_at,
        n.deadline_at
    FROM notices AS n
    JOIN notices_staff AS ns
    ON ns.notice_id = n.notice_id
    WHERE ns.staff_id = %s
    AND ns.read = 0
    """
    cursor.execute(query, (staff_id,))
    return cursor.fetchall()

################################################################################
