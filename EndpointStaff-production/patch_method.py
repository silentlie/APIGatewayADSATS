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
        staff_id = body['staff_id']
        
        # Update name if present in body
        if 'staff_name' in body:
            update_staff_name(cursor,  body['staff_name'],staff_id)

        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], staff_id)
        
        # Update description value if present in body
        if 'description' in body:
            update_description(cursor, body['description'], staff_id)
        
        # Delete existing records then insert new ones if 'aircraft_ids' is in body
        if 'aircraft_ids' in body:
            insert_aircraft_staff(cursor, body['staff_ids'], staff_id)
        
        # Delete existing records then insert new ones if 'aircraft_ids' is in body
        if 'role_ids' in body:
            insert_roles_staff(cursor, body['role_ids'], staff_id)
        
        # Delete existing records then insert new ones if 'aircraft_ids' is in body
        if 'subcategory_ids' in body:
            insert_staff_subcategories(cursor, body['subcategory_ids'], staff_id)
        connection.commit()
        return_body = staff_id
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
def update_staff_name(
    cursor: MySQLCursorAbstract,
    staff_name: str,
    staff_id: int
) -> None:
    """
    Update name
    """
    update_query = """
        UPDATE staff
        SET staff_name = %s
        WHERE staff_id = %s
    """
    params = [staff_name, staff_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_archived(
    cursor: MySQLCursorAbstract,
    archived: int,
    staff_id: int
) -> None:
    """
    Update archived or not
    """
    update_query = """
        UPDATE staff
        SET archived = %s
        WHERE staff_id = %s
    """
    params = [archived, staff_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def update_description(
    cursor: MySQLCursorAbstract,
    description: str,
    staff_id: int
) -> None:
    """
    Update description
    """
    update_query = """
        UPDATE staff
        SET description = %s
        WHERE staff_id = %s
    """
    params = [description, staff_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

@timer
def delete_aircraft_staff(
    cursor: MySQLCursorAbstract,
    staff_id: int
) -> None:
    """
    Delete linking records of specific id
    """
    delete_query = """
        DELETE FROM aircraft_staff
        WHERE staff_id = %s
    """
    params = [staff_id]
    cursor.execute(delete_query, params)
    print(cursor.rowcount, " records deleted successfully")

@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract,
    aircraft_ids: list,
    staff_id :int
):
    """
    Insert into many to many table
    """
    # Delete before insert
    delete_aircraft_staff(cursor, staff_id)
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for aircraft_id in aircraft_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

@timer
def delete_roles_staff(
    cursor: MySQLCursorAbstract,
    staff_id: int
) -> None:
    """
    Delete linking records of specific id
    """
    delete_query = """
        DELETE FROM roles_staff
        WHERE staff_id = %s
    """
    params = [staff_id]
    cursor.execute(delete_query, params)
    print(cursor.rowcount, " records deleted successfully")

@timer
def insert_roles_staff(
    cursor: MySQLCursorAbstract,
    role_ids: list,
    staff_id :int
):
    """
    Insert into many to many table
    """
    # Delete before insert
    delete_roles_staff(cursor, staff_id)
    insert_query = """
        INSERT INTO roles_staff (role_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(role_id, staff_id) for role_id in role_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

@timer
def delete_staff_subcategories(
    cursor: MySQLCursorAbstract,
    staff_id: int
) -> None:
    """
    Delete linking records of specific id
    """
    delete_query = """
        DELETE FROM staff_subcategories
        WHERE staff_id = %s
    """
    params = [staff_id]
    cursor.execute(delete_query, params)
    print(cursor.rowcount, " records deleted successfully")

@timer
def insert_staff_subcategories(
    cursor: MySQLCursorAbstract,
    subcategory_ids: dict,
    staff_id :int
):
    """
    Insert into many to many table
    """
    # Delete before insert
    delete_aircraft_staff(cursor, staff_id)
    insert_query = """
        INSERT INTO staff_subcategories (
            staff_id, 
            subcategory_id, 
            access_level_id
        )
        VALUES (%s, %s)
    """
    records_to_insert = [
        (staff_id, subcategory_id, access_level_id) 
        for subcategory_id, access_level_id 
        in subcategory_ids.items()
    ]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

#===============================================================================