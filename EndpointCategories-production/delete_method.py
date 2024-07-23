from helper import Error, connect_to_db, json_response, timer


@timer
def delete_method(body: dict) -> dict:
    """
    Handles DELETE requests to remove a category record.

    Args:
        body (dict): The request body containing the ID of the category to be deleted.

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
        category_id = body["category_id"]

        # Delete the category with the given ID
        delete_query = """
            DELETE FROM categories
            WHERE category_id = %s
        """
        cursor.execute(delete_query, [category_id])
        connection.commit()

        # Prepare successful response
        return_body = {"category_id": category_id}
        status_code = 200
    # Catch SQL exeption
    except Error as e:
        return_body = {"error": e._full_msg}
        if e.errno == 1062:
            # Code 409 means conflict in the state of the server
            status_code = 409
    # Catch other exeptions
    except Exception as e:
        return_body = {"error": str(e)}
    # Close cursor and connection
    finally:
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
