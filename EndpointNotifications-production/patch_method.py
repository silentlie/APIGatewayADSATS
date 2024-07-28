from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update an existing notice record.

    Args:
        body (dict): The request body containing the notice details to update.

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

        if "notice_id" in body and "staff_id" in body:
            update_notices_staff(cursor, body["staff_id"], body["notice_id"])
        else:
            raise ValueError("Invalid use of method")

        # Commit the transaction
        connection.commit()
        return_body = {"notice_id": body["notice_id"]}
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

    # Create the response and print it
    response = json_response(status_code, return_body)
    print(response)
    return response


@timer
def update_notices_staff(
    cursor: MySQLCursorAbstract, staff_id: int, notice_id: int
) -> None:
    """
    ...

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The ID of the recipient to update.
        notice_id (int): The ID of the notice to update.
    """
    update_query = """
    UPDATE notices_staff
    SET read = 1
    AND read = CURRENT_TIMESTAMP
    WHERE staff_id = %s
    AND notice_id = %s
    """

    # Execute the query
    cursor.execute(update_query, (staff_id, notice_id,))
    print(f"{cursor.rowcount} record(s) successfully updated")


################################################################################
