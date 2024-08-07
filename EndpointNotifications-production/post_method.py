from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new notice record

    Args:
        body (dict): The request body containing the notice details.

    Returns:
        dict: The HTTP response dictionary with status code, headers, and body.
              Includes the newly created 'notice_id' or error details.
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500

    try:
        # Establish database connection
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        if "staff_ids" in body and "notice_id" in body:
            insert_notices_staff(cursor, body["notice_id"], body["staff_ids"])

        # Commit the transaction
        connection.commit()
        return_body = {"notice_id": body["notice_id"]}
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
def insert_notices_staff(
    cursor: MySQLCursorAbstract, notice_id: int, staff_ids: list
) -> None:
    """
    This is the notification table consist notice_id and staff_id, which are the recipients, also whether and when it was read by the recipient
    Inserts records into the notices_staff linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The ID of the notice.
        staff_ids (list): The list of staff IDs to link with the notice.

    Returns:
        None
    """
    insert_query = """
    INSERT INTO notices_staff (notice_id, staff_id, read, read_at)
    VALUES (%s, %s, NULL)
    ON DUPLICATE KEY UPDATE read_at = NULL
    """
    records_to_insert = [(notice_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


################################################################################
