import mysql.connector
import os
import json
from mysql.connector import Error

def patch_method(body):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()
        
        aircraft_id = body['aircraft_id']
        

        if 'archived' in body:
            update_archived_value(cursor, aircraft_id, body['archived'])
            connection.commit()

        if 'name' in body:
            update_aircraft(cursor, body, aircraft_id)
            connection.commit()

        if 'staff' in body:
            pass
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
        print(f"Error: {str(e)}")
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
    aircraft = body["name"]
    
    update_query = """
        UPDATE aircrafts
        SET name = %s
        WHERE aircraft_id = %s
    """
    params = [aircraft, aircraft_id]
    cursor.execute(update_query, params)

def update_archived_value(cursor, aircraft_id, archived):
    
    query = """
        UPDATE aircrafts 
        SET archived = %s
        WHERE aircraft_id = %s
    """
    params = [archived, aircraft_id] 
    cursor.execute(query, params)
