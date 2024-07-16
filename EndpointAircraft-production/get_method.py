from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def get_method(parameters):
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        valid_methods = ["name_only", "aircraft"]
        if 'method' not in parameters or parameters['method'] not in valid_methods:
            raise ValueError("Invalid method")
        elif parameters['method'] == "name_only":
            response = name_only(cursor)
        elif (parameters['method'] == "aircraft"):
            query, params = build_query(parameters)
            response = {}
            response['total_records'] = total_records(cursor, query, params)
            response['aircraft'] = aircraft(cursor, query, params, parameters)
        print(response)
        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(response, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {e._full_msg}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(e._full_msg)
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
            print("MySQL cursor is closed")
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

## FUNCTIONS ##
# build query
def build_query(parameters):
    query = """
    SELECT
        *
    FROM aircraft
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search for name of aircraft
    if 'search' in parameters:
        filters.append("aircraft_name LIKE %s")
        params.append(parameters["search"])
    # filter based on archived or not
    if 'archived' in parameters:
        filters.append("archived = %s")
        params.append(parameters["archived"])
    # filter based on date range when aircraft was added
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

# return dict of total records
def total_records(cursor, query, params):
    total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
    print(total_query)
    print(params)
    cursor.execute(total_query, params)
    return cursor.fetchall()[0]['total_records']

# return dit of all aircraft with pagination
def aircraft(cursor, query, params, parameters):
    # sort column if need it, default is pk of aircraft
    valid_columns = ["aircraft_id", "aircraft_name", "archived", "created_at", "updated_at"]
    valid_orders = ["ASC", "DESC"]
    if 'sort_column' in parameters and 'order' in parameters and parameters['sort_column'] in valid_columns and parameters['order'] in valid_orders:
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

# return dict of aircraft id and name only
def name_only(cursor):
    query = """
    SELECT
        aircraft_id,
        aircraft_name
    FROM aircraft
    """
    cursor.execute(query)
    return cursor.fetchall()

## FUNCTIONS ##

## HELPERS ##
# Create a connection to the DB
def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

# Response headers
def headers():
    return {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': allowed_headers
    }

# for dump datetime json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

## HELPERS ##

# ===========================================================================
# parameters = {
#     'method': "aircraft",
#     'archived': "0",
#     'sort_column': "created_at",
#     'order': "ASC",
#     'limit': 10,
#     'offset': 0
# }
# print(get_method(parameters))