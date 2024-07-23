from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def post_method(body: dict) -> dict:
    """
    Handles POST requests to insert a new staff record and optionally link staff records.

    Args:
        body (dict): The request body containing the staff details and optional linking IDs.

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

        # Insert the new record and get the id
        staff_id = insert_staff(cursor, body)

        # Insert linking records if any aircraft IDs are provided
        if "aircraft_ids" in body:
            insert_aircraft_staff(cursor, staff_id, body["aircraft_ids"])
        # Insert linking records if any role IDs are provided
        if "role_ids" in body:
            insert_roles_staff(cursor, staff_id, body["role_ids"])
        # Insert linking records if any subcategory IDs are provided
        if "subcategory_ids" in body:
            insert_staff_subcategories(cursor, staff_id, body["subcategory_ids"])

        # Commit the transaction
        connection.commit()
        return_body = {"staff_id": staff_id}
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
def insert_staff(cursor: MySQLCursorAbstract, body: dict) -> int:
    """
    Inserts a new staff record into the database.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        body (dict): The request body containing the staff details.

    Returns:
        int: The ID of the newly inserted staff record.
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
        body["updated_at"],
    ]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    assert isinstance(result, dict)
    staff_id = result["id"]
    assert isinstance(staff_id, int)
    print("Record inserted successfully with ID:", staff_id)
    return staff_id


@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract, staff_id: int, aircraft_ids: list
) -> None:
    """
    Inserts records into the aircraft_staff table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The ID of the staff member.
        aircraft_ids (list): The list of aircraft IDs to link with the staff.

    Returns:
        None
    """
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for aircraft_id in aircraft_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


@timer
def insert_roles_staff(
    cursor: MySQLCursorAbstract, staff_id: int, role_ids: list
) -> None:
    """
    Inserts records into the roles_staff table.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The ID of the staff member.
        role_ids (list): The list of role IDs to link with the staff.

    Returns:
        None
    """
    insert_query = """
        INSERT INTO roles_staff (role_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(role_id, staff_id) for role_id in role_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


@timer
def insert_staff_subcategories(
    cursor: MySQLCursorAbstract, staff_id: int, subcategory_ids: dict
) -> None:
    """
    Inserts records into the staff_subcategories table to create associations between staff and subcategories
    with specific access levels.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.
        staff_id (int): The ID of the staff member.
        subcategory_ids (dict): A dictionary where the keys are subcategory IDs and the values are access level IDs.

    Returns:
        None
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
        for subcategory_id, access_level_id in subcategory_ids.items()
    ]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} records successfully inserted")


################################################################################
