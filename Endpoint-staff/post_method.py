import json
from mysql.connector import Error
import mysql.connector
import os
from datetime import datetime
def post_method(body):
    try:
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "adsats_database",
        )
        cursor = connection.cursor()
        check_query = "SELECT COUNT(*) FROM staff WHERE email = %s"
        email = body["email"]
        cursor.execute(check_query, (email,))
        result = cursor.fetchone()

        if result[0] > 0: # type: ignore
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
                'body': json.dumps(f"staff with email '{email}' already exists.")
            }
        print("finish check_query")
        staff_id = insert_and_get_staff_id(cursor, body)
        connection.commit()
        print("finish staff_id")
        if 'aircrafts' in body:
            aircraft_ids = get_aircraft_ids_by_names(cursor, body['aircrafts'])
            insert_staff_aircrafts(cursor, staff_id, aircraft_ids)
            connection.commit()
        
        if 'roles' in body:
            role_ids = get_role_ids_by_names(cursor, body['roles'])
            insert_staff_roles(cursor, staff_id, role_ids)
            connection.commit()

        if 'categories' in body:
            category_ids = get_category_ids_by_names(cursor, body['categories'])
            insert_permissions(cursor, staff_id, category_ids)
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

    created_at = body["created_at"]

    query = """
    INSERT INTO staff (f_name, l_name, email, archived, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, Null)
    """
    params = [f_name, l_name, email, archived, created_at]
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

def get_aircraft_ids_by_names(cursor, aircrafts):
    format_strings = ','.join(['%s'] * len(aircrafts))
    query = f"SELECT aircraft_id FROM aircrafts WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(aircrafts))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_category_ids_by_names(cursor, categories):
    format_strings = ','.join(['%s'] * len(categories))
    query = f"SELECT category_id FROM categories WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(categories))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_staff_roles(cursor, staff_id, role_ids):
    query = "INSERT INTO staff_roles VALUES (%s, %s)"
    for role_id in role_ids:
        cursor.execute(query, (staff_id, role_id))

def insert_staff_aircrafts(cursor, staff_id, aircraft_ids):
    query = "INSERT INTO aircraft_staff VALUES (%s, %s)"
    for aircraft_id in aircraft_ids:
        cursor.execute(query, (aircraft_id, staff_id))

def insert_permissions(cursor, staff_id, category_ids):
    query = "INSERT INTO permissions VALUES (Null, %s, %s)"
    for category_id in category_ids:
        cursor.execute(query, (category_id, staff_id))

# for dump json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)