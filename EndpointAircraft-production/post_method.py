import os
import json
import mysql.connector
from mysql.connector import Error
from lambda_function import allowed_headers

def post_method(body):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        # Insert the new aircraft record and get the aircraft ID
        aircraft_id = insert_aircraft(cursor, body)
        # Link staff to newly added aircraft in table aircraft_staff
        if 'staff_ids' in body:
            insert_aircraft_staff(cursor, aircraft_id, body['staff_ids'])
        # Commits the transaction to make the insert operation permanent
        # If any error is raised, there'll be no commit
        connection.commit()

        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(aircraft_id)
        }
    # Catch SQL exeption
    except Error as e:
        print(f"Error: {e._full_msg}")
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
            'body': json.dumps(f"Error: {e._full_msg}")
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

## FUNCTIONS ##

# Insert new aircraft and return id of that aircraft
def insert_aircraft(cursor, body):
    query = """
    INSERT INTO aircraft (aircraft_name, archived, created_at, description)
    VALUES (%s, %s, %s)
    """
    params = [body["aircraft_name"], body["archived"], body["created_at"], body["description"]]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID()")
    aircraft_id = cursor.fetchone()[0]
    print("Record inserted successfully with ID:", aircraft_id)
    return aircraft_id

# Insert into aircraft_staff
def insert_aircraft_staff(cursor, aircraft_id, staff_ids):
    insert_query = """
        INSERT INTO aircraft_staff (aircraft_id, staff_id)
        VALUES (%s, %s)
    """
    records_to_insert = [(aircraft_id, staff_id) for staff_id in staff_ids]
    cursor.executemany(insert_query, records_to_insert)
    print(cursor.rowcount, " records inserted successfully")

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

## HELPERS ##
#===============================================================================