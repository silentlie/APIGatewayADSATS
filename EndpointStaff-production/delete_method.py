from helper import (
    connect_to_db,
    json_response,
    timer,
    Error
)

@timer
def delete_method(
    body: dict
) -> dict:
    """
    Delete method
    """
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        staff_id = body["staff_id"]

        delete_query = """
            DELETE FROM staff
            WHERE staff_id = %s
        """
        cursor.execute(delete_query, [staff_id])
        connection.commit()
        return_body = staff_id
        status_code = 200
    # Catch SQL exeption
    except Error as e:
        return_body = f"SQL Error: {e._full_msg}"
        # Error no 1062 means duplicate name
        if e.errno == 1062:
            # Code 409 means conflict in the state of the server
            status_code = 409
    # Catch other exeptions
    except Exception as e:
        return_body = f"SQL Error: {e}"
    # Close cursor and connection
    finally:
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    response = json_response(status_code, return_body)
    print (response)
    return response

#===============================================================================