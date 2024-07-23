from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update an existing aircraft record.

    Args:
        body (dict): The request body containing the aircraft details to update.

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

        # Update aircraft fields if present in the request body
        if "aircraft_name" in body:
            update_aircraft_name(cursor, body["aircraft_name"], aircraft_id)

        if "archived" in body:
            update_archived(cursor, body["archived"], aircraft_id)

        if "description" in body:
            update_description(cursor, body["description"], aircraft_id)

        # Handle staff updates
        if "staff_ids" in body:
            # Delete existing staff assignments then insert new ones
            delete_aircraft_staff(cursor, aircraft_id)
            insert_aircraft_staff(cursor, body["staff_ids"], aircraft_id)

        # Commit the transaction
        connection.commit()
        return_body = {"aircraft_id": aircraft_id}
        status_code = 200
    except Error as e:
        # Handle SQL error
        return_body = {"error": e._full_msg}
        if e.errno == 1062:
            status_code = 409  # Conflict error
    except ValueError as e:
        # Handle validation errors
        return_body = {"error": str(e)}
        status_code = 400  # Bad request
    except Exception as e:
        # Handle general error
        return_body = {"error": str(e)}
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")  # Consider using logging instead of print
        if connection and connection.is_connected():
            connection.close()
            print(
                "MySQL connection is closed"
            )  # Consider using logging instead of print

    response = json_response(status_code, return_body)
    print(response)  # Consider using logging instead of print
    return response


@timer
def update_aircraft_name(
    cursor: MySQLCursorAbstract, aircraft_name: str, aircraft_id: int
) -> None:
    """
    Update the name of an aircraft.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        aircraft_name (str): The new name of the aircraft.
        aircraft_id (int): The ID of the aircraft to update.
    """
    query = """
        UPDATE aircraft
        SET aircraft_name = %s
        WHERE aircraft_id = %s
    """
    params = (aircraft_name, aircraft_id)
    cursor.execute(query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def update_archived(
    cursor: MySQLCursorAbstract, archived: int, aircraft_id: int
) -> None:
    """
    Update the archived status of an aircraft.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        archived (int): The new archived status.
        aircraft_id (int): The ID of the aircraft to update.
    """
    query = """
        UPDATE aircraft
        SET archived = %s
        WHERE aircraft_id = %s
    """
    params = (archived, aircraft_id)
    cursor.execute(query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def update_description(
    cursor: MySQLCursorAbstract, description: str, aircraft_id: int
) -> None:
    """
    Update the description of an aircraft.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        description (str): The new description of the aircraft.
        aircraft_id (int): The ID of the aircraft to update.
    """
    query = """
        UPDATE aircraft
        SET description = %s
        WHERE aircraft_id = %s
    """
    params = (description, aircraft_id)
    cursor.execute(query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def delete_aircraft_staff(cursor: MySQLCursorAbstract, aircraft_id: int) -> None:
    """
    Delete all staff assignments for a specific aircraft.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        aircraft_id (int): The ID of the aircraft whose staff assignments will be deleted.
    """
    query = """
        DELETE FROM aircraft_staff
        WHERE aircraft_id = %s
    """
    params = (aircraft_id,)
    cursor.execute(query, params)
    print(f"{cursor.rowcount} record(s) successfully deleted")


@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract, staff_ids: list, aircraft_id: int
) -> None:
    """
    Insert staff assignments into the aircraft_staff table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_ids (list): The list of staff IDs to be assigned to the aircraft.
        aircraft_id (int): The ID of the aircraft.
    """
    query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(query, records_to_insert)
    print(f"{cursor.rowcount} record(s) successfully inserted")
