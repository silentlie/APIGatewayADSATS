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
        # in parameters of method number by default is a str so must convert back to int
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])
        # excute the query
        cursor.execute(query, params)
        # this is get method which return data base on parameters so cursor.fetchall is call
        # but in some method we only need to know if the query is succeed or not
        # use cursor.commit()
        rows = cursor.fetchall()
        response = {
            "total_records": total_records,
            "rows": rows
        }
    # hanlding error
    except Error as e:
        print(f"Error: {e._full_msg}")
        error_message = e._full_msg
    finally:
        # close cursor and connection
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    # if error occur return 500 with error
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

def build_query(parameters):
    query = """
    SELECT aircraft_id, name, status, start_at,end_at
    FROM aircrafts
    """
    
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    if 'aircraft_id' in parameters:
        filters.append("aircraft_id LIKE %s")
        params.append(parameters["name"])
    if 'name' in parameters:
        filters.append("name LIKE %s")
        params.append(parameters["name"]) 
    if 'status' in parameters:
        filters.append("status LIKE %s")
        params.append(parameters["status"]) 
    if 'start_at' in parameters:
        filters.append("start_at LIKE %s")
        params.append(parameters["start_at"])     
    if 'end_at' in parameters:
        filters.append("end_at LIKE %s")
        params.append(parameters["end_at"])  
                 
    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        valid_columns = ["name"]  # Add other valid column names if necessary
        if parameters["sort_column"] in valid_columns:
            order = 'ASC' if parameters.get("asc", 'true') == 'true' else 'DESC'
            query += f" ORDER BY {parameters['sort_column']} {order}"
    
    return query, params

# Create a connection to the DB
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
    query = "SELECT name from aircrafts"
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query)
    response = cursor.fetchall() 
    names = [item[0] for item in response] # type: ignore
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
        'body': json.dumps(names, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
    }

# ===========================================================================


