from helper import (
    connect_to_db,
    json_response,
    timer,
    Error,
    MySQLCursorAbstract
)

@timer
def post_method(
    body: dict
) -> dict:
    """
    Post method
    """
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        # Insert the new record and get the id
        staff_id = insert_staff(cursor, body)
        # Add linking aircraft if any into the table
        if 'aircraft_ids' in body:
            insert_aircraft_staff(cursor, staff_id, body['aircraft_ids'])
        # Add linking role if any into the table
        if 'role_ids' in body:
            insert_roles_staff(cursor, staff_id, body['role_ids'])
        # Add linking subcategories if any into the table
        if 'subcategory_ids' in body:
            insert_staff_subcategories(cursor, staff_id, body['subcategory_ids'])
        # Commits the transaction to make the insert operation permanent
        # If any error is raised, there'll be no commit
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
    return json_response(status_code, return_body)

@timer
def insert_staff(
    cursor: MySQLCursorAbstract,
    body: dict
) -> int:
    """
    Insert new record and return id
    """
    query = """
    INSERT INTO staff (staff_name, email, archived, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = [
        body["staff_name"],
        body["email"],
        body["archived"],
        body["created_at"],
        body["updated_at"]
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID()")
    staff_id = cursor.fetchone()
    assert isinstance(staff_id, int)
    print("Record inserted successfully with ID:", staff_id)
    return staff_id

@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract,
    staff_id: int,
    aircraft_ids: list,
) -> None:
    """
    Insert into many to many table
    """
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [
        (aircraft_id, staff_id) 
        for aircraft_id in aircraft_ids
    ]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

@timer
def insert_roles_staff(
    cursor: MySQLCursorAbstract,
    staff_id: int,
    roles_ids: list,
) -> None:
    """
    Insert into many to many table
    """
    insert_query = """
        INSERT INTO roles_staff (role_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [
        (role_id, staff_id) 
        for role_id in roles_ids
    ]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

@timer
def insert_staff_subcategories(
    cursor: MySQLCursorAbstract,
    staff_id: int,
    subcategory_ids: dict,
) -> None:
    """
    Inserts records into the `staff_subcategories` table to create associations between `staff` and `subcategories`
    with specific `access levels`.

    Parameters:
    - `db_cursor` (`MySQLCursorAbstract`): The MySQL cursor object used to execute the query.
    - `staff_id` (`int`): The ID of the staff member.
    - `subcategory_ids` (`dict`): A dictionary where the keys are subcategory IDs and the values are access level IDs.

    Returns:
    - None

    Raises:
    - `MySQL Error`: If an error occurs during the insertion.
    """
    insert_query = """
        INSERT INTO staff_subcategories (
            staff_id, 
            subcategory_id, 
            access_level_id 
        )
        VALUES (%s, %s, %s)
    """
    records_to_insert = [
        (staff_id, subcategory_id, access_level_id)
        for subcategory_id, access_level_id 
        in subcategory_ids.items()
    ]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

#===============================================================================