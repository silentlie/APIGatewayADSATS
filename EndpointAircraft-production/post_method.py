from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new aircraft record and optionally link staff records.

    Args:
        body (dict): The request body containing the aircraft details and optional staff IDs.

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

        # Insert the new aircraft record and get the ID
        aircraft_id = insert_aircraft(cursor, body)

        # Insert linking records if any staff IDs are provided
        if "staff_ids" in body:
            insert_aircraft_staff(cursor, aircraft_id, body["staff_ids"])

        # Commit the transaction
        connection.commit()
        return_body = {"aircraft_id": aircraft_id}
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
def insert_aircraft(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new aircraft record into the database.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the aircraft details.

    Returns:
        int: The ID of the newly inserted aircraft record.
    """
    query = """
    INSERT INTO aircraft (
        aircraft_name,
        archived,
        created_at,
        description
    )
    VALUES (%s, %s, %s, %s)
    """
    params = [
        body["aircraft_name"],
        body["archived"],
        body["created_at"],
        body["description"],
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict), "Result must be a dict"
    aircraft_id = result["id"]
    assert isinstance(aircraft_id, int), "Aircraft ID must be an integer"
    print("Record inserted successfully with ID: ", aircraft_id)
    return aircraft_id


@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract, aircraft_id: int, staff_ids: list
) -> None:
    """
    Inserts records into the aircraft_staff linking table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        aircraft_id (int): The ID of the aircraft.
        staff_ids (list): The list of staff IDs to link with the aircraft.

    Returns:
        None
    """
    insert_query = """
    INSERT INTO aircraft_staff (aircraft_id, staff_id)
    VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


################################################################################
