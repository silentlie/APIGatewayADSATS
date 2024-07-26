from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new notice record

    Args:
        body (dict): The request body containing the notice details.

    Returns:
        dict: The HTTP response dictionary with status code, headers, and body.
              Includes the newly created 'notice_id' or error details.
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500

    try:
        # Establish database connection
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        # Insert the new notice record and get the ID
        notice_id = insert_notice(cursor, body)

        # Insert linking records if any aircraft IDs are provided
        if "aircraft_ids" in body:
            insert_aircraft_notices(cursor, notice_id, body["aircraft_ids"])
        if "staff_ids" in body:
            insert_notices_staff(cursor, notice_id, body["staff_ids"])

        # Commit the transaction
        connection.commit()
        return_body = {"notice_id": notice_id}
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
def insert_notice(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new notice record into the database.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the notice details.

    Returns:
        int: The ID of the newly inserted notice record.
    """
    query = """
    INSERT INTO notices (
        subject,
        type,
        staff_id,
        archived,
        noticed_at,
        deadline_at,
        details
    )
    VALUES (%s, %s, %s, %s, %s)
    """
    params = [
        body["subject"],
        body["type"],
        body["staff_id"],
        body["archived"],
        body["noticed_at"],
        body["deadline_at"],
        body["details"],
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict), "Result must be a dict"
    notice_id = result["id"]
    assert isinstance(notice_id, int), "notice ID must be an integer"
    print("Record inserted successfully with ID: ", notice_id)
    return notice_id


@timer
def insert_notices_staff(
    cursor: MySQLCursorAbstract, notice_id: int, staff_ids: list
) -> None:
    """
    This is the notification table consist notice_id and staff_id, which are the recipients, also whether and when it was read by the recipient
    Inserts records into the notices_staff linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The ID of the notice.
        staff_ids (list): The list of staff IDs to link with the notice.

    Returns:
        None
    """
    insert_query = """
    INSERT INTO notices_staff (notice_id, staff_id, read, read_at)
    VALUES (%s, %s, 0, NULL)
    ON DUPLICATE KEY UPDATE read = 0, read_at = NULL
    """
    records_to_insert = [(notice_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


@timer
def insert_aircraft_notices(
    cursor: MySQLCursorAbstract, notice_id: int, aircraft_ids: list
) -> None:
    """
    Inserts records into the aircraft_notices linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The ID of the notice.
        aircraft_ids (list): The list of aircraft IDs to link with the notice.

    Returns:
        None
    """
    insert_query = """
    INSERT INTO aircraft_notices (notice_id, aircraft_id)
    VALUES (%s, %s)
    """
    records_to_insert = [(notice_id, aircraft_id) for aircraft_id in aircraft_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully insseted")


@timer
def insert_documents_notices(
    cursor: MySQLCursorAbstract, notice_id: int, documents: list
) -> None:
    """
    Inserts records into the documents_notices linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        notice_id (int): The ID of the notice.
        documents (list): The list of documents to link with the notice.

    Returns:
        None
    """
    insert_query = """
    INSERT INTO documents_notices (notice_id, document_name)
    VALUES (%s, %s)
    """
    records_to_insert = [(notice_id, document_name) for document_name in documents]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully insseted")

################################################################################
