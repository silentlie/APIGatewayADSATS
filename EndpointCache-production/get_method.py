from helper import Error, MySQLCursorAbstract, connect_to_db, json_response, timer


@timer
def get_method(parameters: dict) -> dict:
    """
    Handles GET requests to fetch the names and IDs of staff, aircraft, categories, subcategories, and roles.

    Args:
        parameters (dict): The query parameters for the request.

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

        if "cache" in parameters:
            return_body = {
                "aircraft": fetch_aircraft(cursor),
                "categories": fetch_categories(cursor),
                "subcategories": fetch_subcategories(cursor),
                "staff": fetch_staff(cursor),
                "roles": fetch_roles(cursor),
            }
        else:
            raise ValueError("Invalid use of method: 'cache' parameter is required.")
        
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
def fetch_aircraft(cursor: MySQLCursorAbstract) -> list:
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
def fetch_categories(cursor: MySQLCursorAbstract) -> list:
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
def fetch_subcategories(cursor: MySQLCursorAbstract) -> list:
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
def fetch_staff(cursor: MySQLCursorAbstract) -> list:
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
def fetch_roles(cursor: MySQLCursorAbstract) -> list:
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
