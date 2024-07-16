import os
import json
import mysql.connector
from mysql.connector import Error

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def patch_method(body):
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        subcategory_id = body['subcategory_id']
        
        # Update name if present in body
        if 'subcategory name' in body:
            update_subcategory_name(cursor,  body['subcategory_name'],subcategory_id)

        # Update archived value if present in body
        if 'archived' in body:
            update_archived(cursor, body['archived'], subcategory_id)
        
        # Update description value if present in body
        if 'description' in body:
            update_description(cursor, body['description'], subcategory_id)
        
        # Update category_id if present in body
        if 'category_id' in body:
            update_category_id(cursor, body['category_id'], subcategory_id)

        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(subcategory_id)
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
def update_subcategory_name(cursor, subcategory_name, subcategory_id):
    update_query = """
        UPDATE subcategories
        SET subcategory_name = %s
        WHERE subcategory_id = %s
    """
    params = [subcategory_name, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")
# Update archived or not
def update_archived(cursor, archived, subcategory_id):
    update_query = """
        UPDATE subcategories
        SET archived = %s
        WHERE subcategory_id = %s
    """
    params = [archived, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")
# Update description
def update_description(cursor, description, subcategory_id):
    update_query = """
        UPDATE subcategories
        SET description = %s
        WHERE subcategory_id = %s
    """
    params = [description, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")
# Update category_id
def update_category_id(cursor, category_id, subcategory_id):
    update_query = """
        UPDATE subcategories
        SET category_id = %s
        WHERE subcategory_id = %s
    """
    params = [category_id, subcategory_id]
    cursor.execute(update_query, params)
    print(cursor.rowcount, " records updated successfully")

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