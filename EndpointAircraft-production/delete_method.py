import os
import json
import mysql.connector
from mysql.connector import Error

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def delete_method(body):
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        aircraft_id = body["aircraft_id"]

        delete_query = """
            DELETE FROM aircraft
            WHERE aircraft_id = %s
        """
        cursor.execute(delete_query, [aircraft_id])
        connection.commit()
        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(aircraft_id)
        }
    # Catch SQL exeption
    except Error as e:
        print(f"SQL Error: {e._full_msg}")
        # Error no 1062 means duplicate name
        if e.errno == 1062:
            # Error code 409 means conflict in the state of the server
            error_code = 409
        else:
            # Error code 500 means other errors have not been specified
            error_code = 500
        
        return {
            'statusCode': error_code,
            'headers': headers(),
            'body': json.dumps(f"SQL Error: {e._full_msg}")
        }
    # Catch other exeptions
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(f"Error: {e}")
        }
    # Close cursor and connection
    finally:
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

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

## HELPERS ##
#===============================================================================