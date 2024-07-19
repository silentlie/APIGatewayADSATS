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
        valid_methods = [
            "name_only",
            "roles",
            "specific_role_staff"
        ]
        if (
            'method' not in parameters 
            or parameters['method'] not in valid_methods
        ):
            raise ValueError("Invalid method")
        elif (parameters['method'] == "name_only"):
            return_body = name_only(cursor)
        elif (parameters['method'] == "roles"):
            query, params = build_query(parameters)
            return_body = {}
            return_body['total_records'] = total_records(cursor, query, params)
            return_body['roles'] = roles(cursor, query, params, parameters)
        elif (parameters['method'] == "specific_role_staff"):
            role_id = parameters['role_id']
            cursor = connection.cursor()
            return_body = {
                'staff_ids': specific_role_staff(cursor, role_id)
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
    print (return_body)
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
    FROM roles
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search for name
    if 'search' in parameters:
        filters.append("role_name LIKE %s")
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
    print(query)
    print(params)
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
def roles(
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
        "role_id",
        "role_name",
        "archived",
        "created_at",
        "updated_at"
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
    cursor: MySQLCursorAbstract,
) -> list:
    """
    Return id and name only
    """
    query = """
    SELECT
        role_id,
        role_name
    FROM roles
    """
    cursor.execute(query)
    return cursor.fetchall()

def specific_role_staff(
    cursor: MySQLCursorAbstract,
    role_id: int,
) -> list:
    """
    Return a list of staff linked with specific id
    """
    query = """
    SELECT
        staff_id
    FROM roles_staff
    WHERE role_id = %s
    """
    cursor.execute(query, [role_id])
    return [num for num, in cursor.fetchall()]

#===============================================================================
# parameters = {
#     'method': "specific_role_staff",
#     'role_id': 1
# }
# get_method(parameters)