from helper import (
    connect_to_db,
    json_response,
    timer,
    Error,
    MySQLCursorAbstract
)

@timer
def patch_method(
    body: dict
) -> dict:
    """
    Patch method
    """
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        aircraft_id = body['aircraft_id']
        
        # Update name if present in body
        if 'aircraft_name' in body:
            update_aircraft_name(cursor,  body['aircraft_name'],aircraft_id)

        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], aircraft_id)
        
        # Update description value if present in body
        if 'description' in body:
            update_description(cursor, body['description'], aircraft_id)
        
        # Delete existing staff assignments then insert new ones if 'staff' is in body
        if 'staff_ids' in body:
            insert_aircraft_staff(cursor, body['staff_ids'], aircraft_id)
        connection.commit()
        return_body = aircraft_id
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

@timer
def update_aircraft_name(
    cursor: MySQLCursorAbstract,
    aircraft_name: str,
    aircraft_id: int
) -> None:
    """
    Update name
    """
    update_query = """
        UPDATE aircraft
        SET aircraft_name = %s
        WHERE aircraft_id = %s
    """
    params = [aircraft_name, aircraft_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_archived(
    cursor: MySQLCursorAbstract,
    archived: int,
    aircraft_id: int
) -> None:
    """
    Update archived or not
    """
    update_query = """
        UPDATE aircraft
        SET archived = %s
        WHERE aircraft_id = %s
    """
    params = [archived, aircraft_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    aircraft_id: int
) -> None:
    """
    Update description
    """
    update_query = """
        UPDATE aircraft
        SET description = %s
        WHERE aircraft_id = %s
    """
    params = [description, aircraft_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def delete_aircraft_staff(
    cursor: MySQLCursorAbstract,
    aircraft_id: int
) -> None:
    """
    Delete linking records of specific id
    """
    delete_query = """
        DELETE FROM aircraft_staff
        WHERE aircraft_id = %s
    """
    params = [aircraft_id]
    cursor.execute(delete_query, params)
    print(cursor.rowcount, " records deleted successfully")

@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract,
    staff_ids: list,
    aircraft_id :int
):
    """
    Insert into many to many table
    """
    # Delete before insert
    delete_aircraft_staff(cursor, aircraft_id)
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

#===============================================================================