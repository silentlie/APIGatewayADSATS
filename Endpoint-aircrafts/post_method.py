import mysql.connector
import os
import json
from mysql.connector import Error
from datetime import datetime

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        # Check if the aircraft name already exists
        aircraft_name = body["aircraftName"]
        check_query = "SELECT COUNT(*) FROM aircraft WHERE name = %s"
        cursor.execute(check_query, (aircraft_name,))
        result = cursor.fetchone()

        if result[0] > 0: # type: ignore
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
                'body': json.dumps(f"Aircraft with name '{aircraft_name}' already exists.")
            }

        # Insert the new aircraft record and get the aircraft ID
        aircraft_id = insert_and_get_aircraft_id(cursor, body)
        connection.commit()
        
        # aircraft_staff
        if 'staff' in body:
            staff_ids = get_staff_ids_by_names(cursor, body['staff'])
            insert_aircraft_staff(cursor, aircraft_id, staff_ids)
            connection.commit()
        

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(aircraft_id)
        }

    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(f"Error: {e}")
        }
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insert_and_get_aircraft_id(cursor, body):
    aircraft_name = body["aircraftName"]
    archived = body["archived"]
    created_at = body["created_at"]

    query = """
    INSERT INTO aircraft (name, archived, created_at)
    VALUES (%s, %s, %s)
    """
    params = [aircraft_name, archived, created_at]
    cursor.execute(query, params)
    
    query = "SELECT aircraft_id FROM aircraft WHERE name = %s"
    cursor.execute(query, (aircraft_name,))
    result = cursor.fetchone()
    print(result)
    return result[0]

def get_staff_ids_by_names(cursor, staff):
    format_strings = ','.join(['%s'] * len(staff))
    query = f"SELECT staff_id FROM staff WHERE email IN ({format_strings})"
    cursor.execute(query, tuple(staff))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_aircraft_staff(cursor, aircraft_id, staff_ids):
    query = "INSERT INTO aircraft_staff (aircraft_id, staff_id) VALUES (%s, %s)"
    for staff_id in staff_ids:
        cursor.execute(query, (aircraft_id, staff_id))
        
