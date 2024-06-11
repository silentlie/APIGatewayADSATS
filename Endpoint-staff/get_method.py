from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    if not parameters:
        return get_method_no_parameters()
    try:
        connection = connect_to_db()
        
        if 'email' in parameters:
            cursor = connection.cursor(dictionary=True)
            return get_specific_staff(cursor, parameters)

        query, params = build_query(parameters)
        total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
        cursor = connection.cursor()
        cursor.execute(total_query, params)
        total_records = cursor.fetchone()[0] # type: ignore
        cursor = connection.cursor(dictionary=True)
        query += " LIMIT %s OFFSET %s"
        
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])
        cursor.execute(query, params)
        rows = cursor.fetchall()
        response = {
            "total_records": total_records,
            "rows": rows
        }
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(response, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {e._full_msg}")
        
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(e._full_msg)
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# this is when start to build query
def build_query(parameters):
    # the base query
    query = """
    SELECT 
        staff_id,
        email,
        f_name,
        l_name,
        created_at,
        archived
    FROM staff
    WHERE deleted_at is Null
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search for one or many emails/users/authors/staff
    if 'search' in parameters:
        filters.append("email LIKE %s")
        params.append(parameters["search"])
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"archived = {parameters["archived"]}")
    
    if 'created_at' in parameters:
        created_at = parameters["created_at"].split(',')
        filters.append("created_at BETWEEN %s AND %s")
        params.extend(created_at)
    
    # if there is any filter add base query
    if filters:
        query += " AND " + " AND ".join(filters)
   
    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        # Add other valid column names if necessary
        valid_columns = ["staff_id", "f_name", "l_name", "email", "archived", "created_at"]
        if parameters["sort_column"] in valid_columns:
            # asc if true, desk if false
            order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
            # in this part must parse as str cannot use binding because sort_column cannot be str
            query += f" ORDER BY {parameters["sort_column"]} {order}"
    
    # finish prepare query and params
    print(query)
    print(params)
    return query, params

# create a connect to db
def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

# for dump json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# return a list string for filtering, searching, sending
def get_method_no_parameters():
    try:
        # get all of roles names where it is not archived
        query = "SELECT email from staff WHERE deleted_at IS Null AND archived = false"
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query)
        response = cursor.fetchall() 
        emails = [item[0] for item in response] # type: ignore
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(emails, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
    except Error as e:
        print(f"Error: {e._full_msg}")
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(e._full_msg)
        }

def get_specific_staff(cursor, parameters):
    
    query = """
    SELECT 
        s.staff_id,
        s.email,
        s.f_name,
        s.l_name,
        GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS aircraft,
        GROUP_CONCAT(DISTINCT r.role SEPARATOR ', ') AS roles,
        GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories,
        GROUP_CONCAT(DISTINCT sc.name SEPARATOR ', ') AS subcategories
    FROM staff AS s
    JOIN aircraft_staff AS au
    ON au.staff_id = s.staff_id
    JOIN aircrafts AS a
    ON a.aircraft_id = au.aircraft_id
    JOIN staff_roles AS rs
    ON rs.staff_id = s.staff_id
    JOIN roles AS r
    ON rs.role_id = r.role_id
    LEFT JOIN permissions AS p
    ON p.staff_id = s.staff_id
    LEFT JOIN categories AS c
    ON c.category_id = p.category_id
    LEFT JOIN subcategories AS sc
    ON sc.category_id = c.category_id
    WHERE email = %s AND s.deleted_at IS Null
    GROUP BY s.staff_id
    """
    params= [parameters["email"]]
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
        'body': json.dumps(rows, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
    }

# ===========================================================================