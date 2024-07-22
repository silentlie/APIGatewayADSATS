from helper import (
    connect_to_db, 
    json_response, 
    timer, 
    Error, 
    MySQLCursorAbstract
)

@timer
def get_method(
    parameters: dict
) -> dict:
    """
    Get method
    """
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        # This may not be the optimal way to handle get method with multiple cases
        valid_procedures = [
            "name_only",
            "staff",
            "specific_staff",
        ]
        if (
            'procedure' not in parameters 
            or parameters['procedure'] not in valid_procedures
        ):
            raise ValueError("Invalid procedure")
        elif (parameters['procedure'] == "name_only"):
            return_body = name_only(cursor)
        elif (parameters['procedure'] == "staff"):
            query, params = build_query(parameters)
            return_body = {}
            return_body['total_records'] = total_records(cursor, query, params)
            return_body['staff'] = staff(cursor, query, params, parameters)
        elif (parameters['procedure'] == "specific_staff"):
            staff_id = int(parameters['staff_id'])
            cursor = connection.cursor()
            return_body = {
                'aircraft_ids': specific_aircraft_staff(cursor, staff_id),
                'role_ids': specific_role_staff(cursor,staff_id),
                'subcategory_ids': specific_staff_subcategories(cursor, staff_id),
            }
        status_code = 200
    # Catch SQL exeption
    except Error as e:
        return_body = f"SQL Error: {e._full_msg}"
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
    return_body = json_response(status_code, return_body)
    return return_body

@timer
def build_query(
    parameters: dict
) -> tuple:
    """
    Build and return query and params
    """
    query = """
    SELECT
        *
    FROM staff
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search for name
    if 'search' in parameters:
        filters.append("staff_name LIKE %s")
        params.append(parameters["search"])
    # filter based on archived or not
    if 'archived' in parameters:
        filters.append("archived = %s")
        params.append(parameters["archived"])
    # filter based on date range when it was added
    if 'created_at' in parameters:
        created_at = parameters["start_at"].split(',')
        filters.append("start_at BETWEEN %s AND %s")
        params.extend(created_at)
    # if there is any filter add to query
    if filters:
        query += "WHERE " + " AND ".join(filters)
    # finish prepare query and params
    return query, params

@timer
def total_records(
    cursor: MySQLCursorAbstract, 
    query: str, 
    params: list
) -> int:
    """
    Return total records
    """
    total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
    print(total_query)
    print(params)
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    assert isinstance(result, dict)
    total_records = result['total_records']
    assert isinstance(total_records, int)
    return total_records

@timer
def staff(
    cursor: MySQLCursorAbstract, 
    query: str, 
    params: list, 
    parameters: dict
) -> list:
    """
    Return all rows based on pagination
    """
    # sort column if need it, default is pk
    valid_columns = [
        "staff_id",
        "staff_name",
        "archived",
        "created_at",
        "updated_at",
    ]
    valid_orders = [
        "ASC",
        "DESC"
    ]
    if (
        'sort_column' in parameters 
        and 'order' in parameters 
        and parameters['sort_column'] in valid_columns 
        and parameters['order'] in valid_orders
    ):
        query += " ORDER BY %s %s"
        params.append(parameters['sort_column'])
        params.append(parameters['order'])
    # pagination
    query += " LIMIT %s OFFSET %s "
    params.append(int(parameters["limit"]))
    params.append(int(parameters["offset"]))
    # finish query
    print(query)
    print(params)
    cursor.execute(query, params)
    return cursor.fetchall()

@timer
def name_only(
    cursor: MySQLCursorAbstract
) -> list:
    """
    Return id and name only
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
def specific_aircraft_staff(
    cursor: MySQLCursorAbstract, 
    staff_id: int
) -> list:
    """
    Return a list of aircraft linked with specific id
    """
    query = """
        SELECT
            aircraft_id
        FROM aircraft_staff
        WHERE staff_id = %s
    """
    cursor.execute(query, [staff_id])
    return cursor.fetchall()

@timer
def specific_role_staff(
    cursor: MySQLCursorAbstract, 
    staff_id: int
) -> list:
    """
    Return a list of roles linked with specific id
    """
    query = """
        SELECT
            role_id
        FROM roles_staff
        WHERE staff_id = %s
    """
    cursor.execute(query, [staff_id])
    return cursor.fetchall()

@timer
def specific_staff_subcategories(
    cursor: MySQLCursorAbstract, 
    staff_id: int
) -> list:
    """
    Return a list of subcategories linked with specific id
    """
    query = """
        SELECT
            subcategorie_id,
            access_level_id
        FROM staff_subcategories
        WHERE staff_id = %s
    """
    cursor.execute(query, [staff_id])
    return cursor.fetchall()

# ===========================================================================
# parameters = {
#     'procedure': "staff",
#     'limit': "20",
#     'offset': "0"
# }
# get_method(parameters)