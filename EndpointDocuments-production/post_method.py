from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new document record and optionally link aircraft records.

    Args:
        body (dict): The request body containing the document details and optional aircraft IDs.
                     Must include 'document_name', 'archived', 'created_at', 'staff_id', and 'subcategory_id'.
                     Optionally includes 'staff_ids' for linking aircraft records.

    Returns:
        dict: The HTTP response dictionary with status code, headers, and body.
              Includes the newly created 'document_id' or error details.
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500

    try:
        # Establish database connection
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        # Insert the new document record and get the ID
        document_id = insert_document(cursor, body)

        # Insert linking records if any staff IDs are provided
        if "staff_ids" in body:
            insert_aircraft_documents(cursor, document_id, body["staff_ids"])

        # Commit the transaction
        connection.commit()
        return_body = {"document_id": document_id}
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
def insert_document(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new document record into the database.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the document details.

    Returns:
        int: The ID of the newly inserted document record.
    """
    query = """
    INSERT INTO documents (
        document_name,
        archived,
        created_at,
        staff_id,
        subcategory_id
    )
    VALUES (%s, %s, %s, %s, %s)
    """
    params = [
        body["document_name"],
        body["archived"],
        body["created_at"],
        body["staff_id"],
        body["subcategory_id"],
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict), "Result must be a dict"
    document_id = result["id"]
    assert isinstance(document_id, int), "document ID must be an integer"
    print("Record inserted successfully with ID: ", document_id)
    return document_id


@timer
def insert_aircraft_documents(
    cursor: MySQLCursorAbstract, document_id: int, aircraft_ids: list
) -> None:
    """
    Inserts records into the aircraft_documents linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        document_id (int): The ID of the document.
        aircraft_ids (list): The list of aircraft IDs to link with the document.

    Returns:
        None
    """
    insert_query = """
    INSERT INTO aircraft_documents (document_id, aircraft_id)
    VALUES (%s, %s)
    """
    records_to_insert = [(document_id, aircraft_id) for aircraft_id in aircraft_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


################################################################################
