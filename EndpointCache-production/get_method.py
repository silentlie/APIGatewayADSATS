from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def get_method(parameters: dict) -> dict:
    """
    return names and ids of staff, aircraft, categories, subcategories, roles
    """
    connection = None
    cursor = None
    return_body = None
    status_code = 500

    try:
        # Establish database connection
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        if "cache" in parameters:
            return {
                "aircraft": aircraft(cursor),
                "categories": categories(cursor),
                "subcategories": subcategories(cursor),
                "staff": staff(cursor),
                "roles": roles(cursor),
            }
        else:
            raise ValueError("Invalid use of method")

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

    response = json_response(status_code, return_body)
    print(response)
    return response


@timer
def aircraft(cursor: MySQLCursorAbstract) -> list:
    """
    Fetches only the aircraft ID and name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.

    Returns:
        list: The list of aircraft IDs and names.
    """
    query = """
    SELECT
        aircraft_id,
        aircraft_name
    FROM aircraft
    """
    cursor.execute(query)
    return cursor.fetchall()


@timer
def categories(cursor: MySQLCursorAbstract) -> list:
    """
    Fetches only the category ID and name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.

    Returns:
        list: The list of category IDs and names.
    """
    query = """
    SELECT
        category_id,
        category_name
    FROM categories
    """
    cursor.execute(query)
    return cursor.fetchall()


@timer
def subcategories(cursor: MySQLCursorAbstract) -> list:
    """
    Fetches only the subcategory ID and name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.

    Returns:
        list: The list of subcategory IDs and names.
    """
    query = """
    SELECT
        subcategory_id,
        subcategory_name
    FROM subcategories
    """
    cursor.execute(query)
    return cursor.fetchall()


@timer
def staff(cursor: MySQLCursorAbstract) -> list:
    """
    Fetches only the staff ID and name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.

    Returns:
        list: The list of staff IDs and names.
    """
    query = """
    SELECT
        staff_id,
        staff_name
    FROM staff
    """
    cursor.execute(query)
    return cursor.fetchall()


@timer
def roles(
    cursor: MySQLCursorAbstract,
) -> list:
    """
    Fetches only the role ID and name.

    Args:
        cursor (MySQLCursorAbstract): The database cursor for executing queries.

    Returns:
        list: The list of role IDs and names.
    """
    query = """
    SELECT
        role_id,
        role_name
    FROM roles
    """
    cursor.execute(query)
    return cursor.fetchall()


################################################################################
