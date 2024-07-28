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

        # Ensure notice_id is in body
        if "notice_id" not in body:
            raise ValueError("Missing notice_id in the request body")

        notice_id = body["notice_id"]

        updatable_fields = [
            "subject",
            "staff_id",
            "archived",
            "details",
            "noticed_at",
            "deadline_at",
        ]
        # Update notice fields if present in the request body
        update_data = {key: body[key] for key in body if key in  updatable_fields}
        if update_data:
            update_notice(cursor, update_data, notice_id)
        if "aircraft" in body:
            delete_aircraft_notices(cursor, notice_id)
            insert_aircraft_notices(cursor, body["aircraft"], notice_id)
        if "delete_documents" in body:
            delete_documents_notices(cursor, body["delete_documents"], notice_id)
        if "insert_documents" in body:
            insert_documents_notices(cursor, body["insert_documents"], notice_id)

        # Commit the transaction
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


@timer
def update_notice(cursor: MySQLCursorAbstract, update_data: dict, notice_id: int) -> None:
    """
    Updates the 'notices' table for a specific notice_id with the provided data.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        update_data (dict):
        notice_id (int): The ID of the notice to update.
    """
    # Extract the fields and params from the dictionary
    fields = update_data.keys()
    params = list(update_data.values())  # Convert dict values to a list of params
    # Create the SET clause dynamically based on the provided fields
    set_clause = ", ".join([f"{field} = %s" for field in fields])

    # Create the update query
    update_query = f"""
        UPDATE notices
        SET {set_clause}
        WHERE notice_id = %s
    """

    # Add the notice_id to the end of the params list
    params.append(notice_id)

    # Execute the query
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def delete_aircraft_notices(cursor: MySQLCursorAbstract, notice_id: int) -> None:
    """
    ...

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries
        notice_id (int): The ID of the notice
    """
    query = """
        DELETE FROM aircraft_notices
        WHERE aircraft_id = %s
    """
    params = (notice_id,)
    cursor.execute(query, params)
    print(f"{cursor.rowcount} record(s) successfully deleted")


@timer
def insert_aircraft_notices(
    cursor: MySQLCursorAbstract, aircraft_ids: list, notice_id: int
) -> None:
    """
    ...

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries
        aircraft_ids (list): ...
        notice_id (int): The ID of the notice
    """
    query = """
        INSERT INTO aircraft_notices (notice_id, aircraft_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(notice_id, aircraft_id) for aircraft_id in aircraft_ids]
    cursor.executemany(query, records_to_insert)
    print(f"{cursor.rowcount} record(s) successfully inserted")


@timer
def delete_documents_notices(
    cursor: MySQLCursorAbstract, documents: list, notice_id: int
) -> None:
    """
    ...

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries
        notice_id (int): The ID of the notice
    """
    query = """
        DELETE FROM documents_notices
        WHERE notice_id = %s
        AND document_name = %s
    """
    records_to_delete = [(notice_id, document_name) for document_name in documents]
    cursor.executemany(query, records_to_delete)
    print(f"{cursor.rowcount} record(s) successfully deleted")


@timer
def insert_documents_notices(
    cursor: MySQLCursorAbstract, documents: list, notice_id: int
) -> None:
    """
    Inserts records into the documents_notices linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries
        notice_id (int): The ID of the notice
        documents (list): The list of documents to link with the notice.
    Returns:
        None
    """
    query = """
        INSERT INTO documents_notices (notice_id, document_name)
        VALUES (%s, %s)
    """
    records_to_insert = [(notice_id, document_name) for document_name in documents]
    cursor.executemany(query, records_to_insert)
    print(f"{cursor.rowcount} record(s) successfully inserted")


################################################################################
