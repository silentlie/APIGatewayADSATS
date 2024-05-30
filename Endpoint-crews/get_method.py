from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    if not parameters:
        return get_method_no_parameters()
    error_message = ""
    try:
        connection = connect_to_db()
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
    except Error as e:
        print(f"Error: {e._full_msg}")
        error_message = e._full_msg
    finally:
       
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    if error_message:
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(error_message)
        }
    # if succeed return 200 with data
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
        'body': json.dumps(response, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
    }

# this is when start to build query
def build_query(parameters):
    # the base query
    query = """
    SELECT 
        user_id,
        email,
        f_name,
        l_name,
        created_at,
        deleted_at,
        modified_at,
        status
    FROM users
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
   # search for one or many emails/users/authors
    if 'user_id' in parameters:
        filters.append("user_id LIKE %s")
        params.append(parameters["user_id"])
        
    if 'email' in parameters:
        filters.append("email LIKE %s")
        params.append(parameters["email"])    
    
    if 'status' in parameters:
        filters.append("status LIKE %s")
        params.append(parameters["status"]) 
    
    if 'created_at' in parameters:
        filters.append("create_at LIKE %s")
        params.append(parameters["create_at"])
    
    if 'modified_at' in parameters:
        filters.append("modified_at LIKE %s")
        params.append(parameters["modified_at"])
    
    if  'deleted_at' in parameters:
        filters.append("delete_at LIKE %s")
        params.append(parameters["delete_at"])  
    
    # if there is any filter add base query
    # if filters:
    #     query += " WHERE " + " AND ".join(filters)
    
   
    if 'sort_column' in parameters:
        # asc if true, desk if false
        order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
        # in thid part must parse as str cannot use binding because sort_column cannot be str
        query += f" ORDER BY {parameters["sort_column"]} {order}"
    
    # finish prepare query and params
    return query, params

# create a connect to db
def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def get_method_no_parameters():
    query = "SELECT email from users"
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

