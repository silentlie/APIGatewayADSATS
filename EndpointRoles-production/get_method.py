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
      
        query, params = build_query(parameters)
        
        total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
        cursor = connection.cursor()
        cursor.execute(total_query, params)
        total_records = cursor.fetchone()[0] # type: ignore
        cursor = connection.cursor(dictionary=True)
        
        query += " LIMIT %s OFFSET %s"
        # in parameters of method number by default is a str so must convert back to int
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
        role_id,
        role,
        archived,
        description,
        created_at
    FROM roles
    """
    query += " WHERE deleted_at is Null"
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search for name of role
    if 'role' in parameters:
        filters.append("role LIKE %s")
        params.append(parameters["role"])
    # filter based on archived or not
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"archived = {parameters["archived"]}")
    # filter based on date range
    if 'created_at' in parameters:
        created_at = parameters["start_at"].split(',')
        filters.append("start_at BETWEEN %s AND %s")
        params.extend(created_at)
    # if there is any filter add base query
    if filters:
        query += " AND " + " AND ".join(filters)
    # if sorting is required
    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        # Add other valid column names if necessary
        valid_columns = ["role_id", "role", "archived", "description"]
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
        query = "SELECT role from roles"
        query += " WHERE archived = false"
        query += " AND deleted_at IS null"
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query)
        response = cursor.fetchall() 
        roles = [item[0] for item in response] # type: ignore
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(roles, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
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
    
# ===========================================================================