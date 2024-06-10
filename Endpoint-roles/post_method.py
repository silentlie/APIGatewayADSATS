import json
from mysql.connector import Error
import mysql.connector
import os
from datetime import datetime

def post_method(body):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()
        role_id = insert_and_get_role_id(cursor, body)
        connection.commit()

        if 'emails' in body and body['emails']:
            staff_ids = get_staff_ids_by_names(cursor, body['emails'])
            insert_staff_roles(cursor, role_id, staff_ids)
            connection.commit()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps({"role_id": role_id}, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }

    except Error as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(str(e))
        }

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def insert_and_get_role_id(cursor, body):
    role = body["role"]
    description = body["description"]
    archived = body["archived"]

    query = """
    INSERT INTO roles (role, description, archived, created_at)
    VALUES (%s, %s, %s, %s)
    """
    params = [role, description, archived, datetime.now()]
    cursor.execute(query, params)

    cursor.execute("SELECT LAST_INSERT_ID()")
    result = cursor.fetchone()
    return result[0]

def get_staff_ids_by_names(cursor, emails):
    format_strings = ','.join(['%s'] * len(emails))
    query = f"SELECT staff_id FROM staff WHERE email IN ({format_strings})"
    cursor.execute(query, tuple(emails))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_staff_roles(cursor, role_id, staff_ids):
    query = """INSERT INTO staff_roles (staff_id, role_id) 
               VALUES (%s, %s)"""
    for staff_id in staff_ids:
        cursor.execute(query, (staff_id, role_id))

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
