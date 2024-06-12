import mysql.connector
import os
import json
from mysql.connector import Error

def patch_method(body):
    connection = None
    cursor = None
    try:
        # # Validate input body
        # required_fields = ['aircraft_id']
        # for field in required_fields:
        #     if field not in body:
        #         raise ValueError(f"Missing required field: {field}")

        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        aircraft_id = body['aircraft_id']

        # Update archived value if present in body
        if 'archived' in body:
            update_archived_value(cursor, aircraft_id, body['archived'])
            connection.commit()

        # Update aircraft name if present in body
        if 'name' in body:
            update_aircraft(cursor, body, aircraft_id)
            connection.commit()

        # Delete existing staff assignments and insert new ones if 'staff' is in body
        if 'staff' in body:
            delete_staff_assignments(cursor, aircraft_id)
            connection.commit()
            staff_ids = select_staff_ids(cursor, body['staff'])
            insert_staff_assignments(cursor, staff_ids, aircraft_id)
            connection.commit()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps({aircraft_id})
        }

    except ValueError as ve:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps({"error": str(ve)})
        }

    except Error as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps({"error": str(e)})
        }

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def update_aircraft(cursor, body, aircraft_id):
    name = body.get("name")

    if name is not None:
        update_query = """
            UPDATE aircrafts
            SET name = %s
            WHERE aircraft_id = %s
        """
        params = [name, aircraft_id]
        cursor.execute(update_query, params)

def update_archived_value(cursor, aircraft_id, archived):
    update_query = """
        UPDATE aircrafts 
        SET archived = %s
        WHERE aircraft_id = %s
    """
    params = [archived, aircraft_id]
    cursor.execute(update_query, params)

def delete_staff_assignments(cursor, aircraft_id):
    delete_query = """
        DELETE FROM aircraft_staff
        WHERE aircraft_id = %s
    """
    params = [aircraft_id]
    cursor.execute(delete_query, params)

def select_staff_ids(cursor, staff_emails):
    staff_ids = []
    for email in staff_emails:
        select_query = """
            SELECT staff_id
            FROM staff
            WHERE email = %s
        """
        cursor.execute(select_query, (email,))
        result = cursor.fetchone()
        if result:
            staff_ids.append(result[0])
    return staff_ids

def insert_staff_assignments(cursor, staff_ids, aircraft_id):
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    for staff_id in staff_ids:
        params = (aircraft_id, staff_id)
        cursor.execute(insert_query, params)
