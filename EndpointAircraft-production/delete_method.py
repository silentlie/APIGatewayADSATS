from helper import Error, connect_to_db, json_response, timer


@timer
def delete_method(body: dict) -> dict:
    """
    Handles DELETE requests to remove an aircraft record from the database.

    Args:
        body (dict): The request body containing the aircraft ID to delete.

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

        # Ensure aircraft_id is in body
        if "aircraft_id" not in body:
            raise ValueError("Missing aircraft_id in the request body")

        aircraft_id = body["aircraft_id"]

        # Execute the delete query
        delete_query = """
            DELETE FROM aircraft
            WHERE aircraft_id = %s
        """
        cursor.execute(delete_query, [aircraft_id])
        connection.commit()

        # Prepare the response
        return_body = {"aircraft_id": aircraft_id}
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
