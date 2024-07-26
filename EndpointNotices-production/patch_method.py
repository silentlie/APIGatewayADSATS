from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update an existing document record.

    Args:
        body (dict): The request body containing the document details to update.
                     Must include 'document_id' and optionally 'archived'.

    Returns:
        dict: The HTTP response dictionary with status code, headers, and body.
              Includes the updated 'document_id' or error details.
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500

    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        # Ensure document_id is in body
        if "document_id" not in body:
            raise ValueError("Missing document_id in the request body")

        document_id = body["document_id"]

        # Update document fields if present in the request body
        if "archived" in body:
            update_archived(cursor, body["archived"], document_id)

        # Commit the transaction
        connection.commit()
        return_body = {"document_id": document_id}
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
def update_archived(
    cursor: MySQLCursorAbstract, archived: int, document_id: int
) -> None:
    """
    Update the archived status of a document.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        archived (int): The new archived status (e.g., 0 for not archived, 1 for archived).
        document_id (int): The ID of the document to update.
    """
    update_query = """
        UPDATE documents
        SET archived = %s
        WHERE document_id = %s
    """
    params = [archived, document_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


################################################################################
