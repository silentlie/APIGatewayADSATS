import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

# Endpoint > /notices/notice-to-crew
# This will create a new notice record
# Then will create a new notice_details record

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "adsats_database",
        )
        cursor = connection.cursor()
        staff_id = insert_and_get_staff_id(cursor, body)
        connection.commit()

        if 'emails' in body:
            aircraft_ids = get_aircraft_ids_by_names(cursor, body['aircraft'])
            insert_staff_aircraft(cursor, staff_id, aircraft_ids)
            connection.commit()
        
        if 'roles' in body:
            role_ids = get_role_ids_by_names(cursor, body['roles'])
            insert_staff_roles(cursor, staff_id, role_ids)
            connection.commit()

        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(staff_id, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
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

def insert_and_get_staff_id(cursor, body):
    # required
    f_name = body["f_name"]
    # required
    l_name = body["l_name"]
    # required
    email = body["email"]
    # required
    archived = body["archived"]
    # TODO:need to check if email is exist

    query = """
    INSERT INTO staff (f_name, l_name, email, archived, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, Null)
    """
    params = [f_name, l_name, email, archived, datetime.datetime.now()]
    cursor.execute(query, params)
    
    query = "SELECT staff_id FROM staff WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    print(result)
    return result[0]

def get_role_ids_by_names(cursor, roles):
    format_strings = ','.join(['%s'] * len(roles))
    query = f"SELECT role_id FROM roles WHERE role IN ({format_strings})"
    cursor.execute(query, tuple(roles))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_aircraft_ids_by_names(cursor, aircraft):
    format_strings = ','.join(['%s'] * len(aircraft))
    query = f"SELECT aircraft_id FROM aircraft WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(aircraft))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_staff_roles(cursor, staff_id, role_ids):
    query = "INSERT INTO staff_roles VALUES (%s, %s)"
    for role_id in role_ids:
        cursor.execute(query, (staff_id, role_id))

def insert_staff_aircraft(cursor, staff_id, aircraft_ids):
    query = "INSERT INTO aircraft_crew VALUES (%s, %s)"
    for aircraft_id in aircraft_ids:
        cursor.execute(query, (aircraft_id, staff_id))

# for dump json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)