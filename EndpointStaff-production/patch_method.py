from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def patch_method(body: dict) -> dict:
    """
    Handles PATCH requests to update an existing staff record.

    Args:
        body (dict): The request body containing the staff details to update.

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

        # Ensure staff_id is in body
        if "staff_id" not in body:
            raise ValueError("Missing staff_id in the request body")

        staff_id = body["staff_id"]

        # Update staff fields if present in the request body
        if "staff_name" in body:
            update_staff_name(cursor, body["staff_name"], staff_id)
        if "archived" in body:
            update_archived(cursor, body["archived"], staff_id)
        if "description" in body:
            update_description(cursor, body["description"], staff_id)
        if "aircraft_ids" in body:
            insert_aircraft_staff(cursor, body["aircraft_ids"], staff_id)
        if "role_ids" in body:
            insert_roles_staff(cursor, body["role_ids"], staff_id)
        if "subcategory_ids" in body:
            insert_staff_subcategories(cursor, body["subcategory_ids"], staff_id)

        # Commit the transaction
        connection.commit()
        return_body = {"staff_id": staff_id}
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
def update_staff_name(
    cursor: MySQLCursorAbstract, staff_name: str, staff_id: int
) -> None:
    """
    Update staff name.
    """
    update_query = """
        UPDATE staff
        SET staff_name = %s
        WHERE staff_id = %s
    """
    params = [staff_name, staff_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def update_archived(cursor: MySQLCursorAbstract, archived: int, staff_id: int) -> None:
    """
    Update archived status.
    """
    update_query = """
        UPDATE staff
        SET archived = %s
        WHERE staff_id = %s
    """
    params = [archived, staff_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def update_description(
    cursor: MySQLCursorAbstract, description: str, staff_id: int
) -> None:
    """
    Update description.
    """
    update_query = """
        UPDATE staff
        SET description = %s
        WHERE staff_id = %s
    """
    params = [description, staff_id]
    cursor.execute(update_query, params)
    print(f"{cursor.rowcount} record(s) successfully updated")


@timer
def delete_aircraft_staff(cursor: MySQLCursorAbstract, staff_id: int) -> None:
    """
    Delete linking records for aircraft.
    """
    delete_query = """
        DELETE FROM aircraft_staff
        WHERE staff_id = %s
    """
    params = [staff_id]
    cursor.execute(delete_query, params)
    print(f"{cursor.rowcount} record(s) successfully deleted")


@timer
def insert_aircraft_staff(
    cursor: MySQLCursorAbstract, aircraft_ids: list, staff_id: int
) -> None:
    """
    Insert into many-to-many table for aircraft.
    """
    # Delete before insert
    delete_aircraft_staff(cursor, staff_id)
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for aircraft_id in aircraft_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} record(s) successfully inserted")


@timer
def delete_roles_staff(cursor: MySQLCursorAbstract, staff_id: int) -> None:
    """
    Delete linking records for roles.
    """
    delete_query = """
        DELETE FROM roles_staff
        WHERE staff_id = %s
    """
    params = [staff_id]
    cursor.execute(delete_query, params)
    print(f"{cursor.rowcount} record(s) successfully deleted")


@timer
def insert_roles_staff(
    cursor: MySQLCursorAbstract, role_ids: list, staff_id: int
) -> None:
    """
    Insert into many-to-many table for roles.
    """
    # Delete before insert
    delete_roles_staff(cursor, staff_id)
    insert_query = """
        INSERT INTO roles_staff (role_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(role_id, staff_id) for role_id in role_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(f"{cursor.rowcount} record(s) successfully inserted")


@timer
def delete_staff_subcategories(cursor: MySQLCursorAbstract, staff_id: int) -> None:
    """
    Delete linking records for subcategories.
    """
    delete_query = """
        DELETE FROM staff_subcategories
        WHERE staff_id = %s
    """
    params = [staff_id]
    cursor.execute(delete_query, params)
    print(f"{cursor.rowcount} record(s) successfully deleted")


@timer
def insert_staff_subcategories(
    cursor: MySQLCursorAbstract, subcategory_ids: dict, staff_id: int
) -> None:
    """
    Insert into many-to-many table for staff subcategories.
    """
    # Delete before insert
    delete_staff_subcategories(cursor, staff_id)
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
    print(f"{cursor.rowcount} record(s) successfully inserted")


################################################################################
