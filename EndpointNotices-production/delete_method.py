from helper import Error, connect_to_db, json_response, timer


@timer
def delete_method(body: dict) -> dict:
    """
    Handles DELETE requests to remove a notice record from the database.

    Args:
        body (dict): The request body containing the notice ID to delete.

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

        # Ensure notice_id is in body
        if "notice_id" not in body:
            raise ValueError("Missing notice_id in the request body")

        notice_id = body["notice_id"]

        delete_query = """
            DELETE FROM notices
            WHERE notice_id = %s
        """
        cursor.execute(delete_query, [notice_id])
        connection.commit()
        return_body = {"notice_id": notice_id}
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


################################################################################
