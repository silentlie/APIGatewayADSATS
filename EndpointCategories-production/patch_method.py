import os
import json
import mysql.connector
from mysql.connector import Error

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def patch_method(body):
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        category_id = body['category_id']
        
        # Update name if present in body
        if 'category name' in body:
            update_category_name(cursor,  body['category_name'],category_id)

        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], category_id)
        
        # Update description value if present in body
        if 'description' in body:
            update_archived(cursor, body['description'], category_id)

        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(category_id)
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

# Update name
def update_category_name(cursor, category_name, category_id):
    update_query = """
        UPDATE categories
        SET category_name = %s
        WHERE category_id = %s
    """
    params = [category_name, category_id]
    cursor.execute(update_query, params)
# Update archived or not
def update_archived(cursor, archived, category_id):
    update_query = """
        UPDATE categories
        SET archived = %s
        WHERE category_id = %s
    """
    params = [archived, category_id]
    cursor.execute(update_query, params)
# Update description
def update_description(cursor, description, category_id):
    update_query = """
        UPDATE categories
        SET description = %s
        WHERE category_id = %s
    """
    params = [description, category_id]
    cursor.execute(update_query, params)

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