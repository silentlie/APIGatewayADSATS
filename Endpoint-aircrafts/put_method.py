import mysql.connector
import os
import json
from mysql.connector import Error

def put_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        aircraft_id = body["aircraft_id"]
        new_aircraft = body["new_aircraft"]
        new_archived = body["new_archived"]

        if new_aircraft is None or new_archived is None or aircraft_id is None:
            return {
                'statusCode': 400,
                'body': "Invalid input: aircraft_id, new_aircraft, and new_archived must be provided"
            }

        # Convert string "true" or "false" to boolean value
        new_archived = True if new_archived.lower() == "true" else False

        update_query = """
                UPDATE aircrafts
                SET name = %s,
                    archived = %s
                WHERE aircraft_id = %s
                """

        cursor.execute(update_query, (new_aircraft, new_archived, aircraft_id))
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': "Internal server error"
        }
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
        },
        'body': "Succeed"
    }
