from helper import Error, connect_to_db, json_response, timer


@timer
def delete_method(body: dict) -> dict:
    """
    Handles DELETE requests to remove a subcategory record.

    Args:
        body (dict): The request body containing the ID of the subcategory to be deleted.

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

        # Ensure category_id is in body
        if "subcategory_id" not in body:
            raise ValueError("Missing subcategory_id in the request body")

        subcategory_id = body["subcategory_id"]

        # Delete the subcategory with the given ID
        delete_query = """
            DELETE FROM subcategories
            WHERE subcategory_id = %s
        """
        cursor.execute(delete_query, [subcategory_id])
        connection.commit()

        # Prepare successful response
        return_body = {"subcategory_id": subcategory_id}
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

    # Return the JSON response
    response = json_response(status_code, return_body)
    print(response)
    return response


################################################################################
