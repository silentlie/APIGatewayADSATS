from helper import (
    connect_to_db,
    json_response,
    timer,
    Error
)

@timer
def delete_method(body: dict) -> dict:
    """
    Handles DELETE requests to remove a role record.

    Args:
        body (dict): The request body containing the ID of the role to be deleted.

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

        # Ensure role_id is in body
        if "role_id" not in body:
            raise ValueError("role_id is required")
        
        role_id = body["role_id"]

        # Delete the role with the given ID
        delete_query = """
            DELETE FROM roles
            WHERE role_id = %s
        """
        cursor.execute(delete_query, [role_id])
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

################################################################################