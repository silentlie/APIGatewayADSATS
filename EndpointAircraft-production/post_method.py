from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Post method
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        # Insert the new record and get the id
        aircraft_id = insert_aircraft(cursor, body)
        # Add linking records if any into the table
        if "staff_ids" in body:
            insert_aircraft_staff(cursor, aircraft_id, body["staff_ids"])
        # Commits the transaction to make the insert operation permanent
        # If any error is raised, there'll be no commit
        connection.commit()
        return_body = aircraft_id
        status_code = 200
    # Catch SQL exeption
    except Error as e:
        return_body = {"error": e._full_msg}
        if e.errno == 1062:
            # Code 409 means conflict in the state of the server
            status_code = 409
    # Catch other exeptions
    except Exception as e:
        return_body = {"error": e}
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


@timer
def insert_aircraft(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Insert new record and return id
    """
    query = """
    INSERT INTO aircraft (aircraft_name, archived, created_at, description)
    VALUES (%s, %s, %s, %s)
    """
    params = [
        body["aircraft_name"],
        body["archived"],
        body["created_at"],
        body["description"],
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID()")
    aircraft_id = cursor.fetchone()
    assert isinstance(aircraft_id, int)
    print("Record inserted successfully with ID:", aircraft_id)
    return aircraft_id


@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract, aircraft_id: int, staff_ids: list
) -> None:
    """
    Insert into many to many table
    """
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

################################################################################
