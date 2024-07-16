import os
import json
import mysql.connector
from mysql.connector import Error
from lambda_function import allowed_headers

def patch_method(body):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        aircraft_id = body['aircraft_id']
        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], aircraft_id)

        # Update aircraft name if present in body
        if 'aircraft name' in body:
            update_aircraft_name(cursor,  body['aircraft_name'],aircraft_id)

        # Delete existing staff assignments and insert new ones if 'staff' is in body
        if 'staff_ids' in body:
            insert_aircraft_staff(cursor, body['staff_ids'], aircraft_id)
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

# Update aircraft name
def update_aircraft_name(cursor, aircraft_name, aircraft_id):
    update_query = """
        UPDATE aircraft
        SET aircraft_name = %s
        WHERE aircraft_id = %s
    """
    params = [aircraft_name, aircraft_id]
    cursor.execute(update_query, params)
# Update archived or not
def update_archived(cursor, archived, aircraft_id):
    update_query = """
        UPDATE aircraft
        SET archived = %s
        WHERE aircraft_id = %s
    """
    params = [archived, aircraft_id]
    cursor.execute(update_query, params)
# Delete linking records of specific aircraft
def delete_aircraft_staff(cursor, aircraft_id):
    delete_query = """
        DELETE FROM aircraft_staff
        WHERE aircraft_id = %s
    """
    params = [aircraft_id]
    cursor.execute(delete_query, params)
# Insert into aircraft_staff
def insert_aircraft_staff(cursor, staff_ids, aircraft_id):
    # Delete before insert
    delete_aircraft_staff(cursor, aircraft_id)
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