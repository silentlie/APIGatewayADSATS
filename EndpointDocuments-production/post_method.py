import json
from mysql.connector import Error
import mysql.connector
import os
from datetime import datetime

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )

        if 'file_name' in body and 'author' in body and 'subcategory' in body:

            cursor = connection.cursor()

            # Insert the new document record
            document_id = insert_and_get_document_id(cursor, body)

            # Insert linked aircraft_document table records if 1 or more aircraft have been selected
            if 'aircraft' in body:
                aircraft_ids = get_aircraft_ids_by_names(cursor, body['aircraft'])
                insert_aircraft_document(cursor, document_id, aircraft_ids)
            
            
            # Complete the commit only after all transactions have been successfully excecuted
            # Commit changes to the database
            connection.commit()

            # Update successful message
            print("Database updated.")

            return {
                'statusCode': 200,
                'headers': headers(),
                'body': json.dumps(document_id)
            }

        return {
            'statusCode': 400,
                'headers': headers(),
                'body': json.dumps('Missing body parameters: Request must include file_name, author, subcategory')
        }

    except mysql.connector.Error as e:
        # Update failed message as an error
        print(f"Database update failed: {e}")

        # Reverting changes because of exception
        connection.rollback()
        return server_error(e)

    except Exception as e:
        print(f"Error: {e}")
        return server_error(e)
        
    finally:
        # Close the cursor
        if cursor:
            cursor.close()

        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
 
# Insert document record
def insert_and_get_document_id(cursor, body):
    file_name = body["file_name"]
    created_at = body['created_at'] if 'created_at' in body else datetime.now()
    archived = 1 if body["archived"] else 0
    author_id = get_author_id(cursor, body["author"])
    subcategory_id = get_subcategory_id(cursor, body["subcategory"])

    # SQL query
    query = """
        INSERT INTO documents 
            (author_id, subcategory_id, file_name, archived, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = [author_id, subcategory_id, file_name, archived, created_at]
    cursor.execute(query, params)
    return cursor.lastrowid

## Insert linking table records ##
# Insert aircraft_document records
def insert_aircraft_document(cursor, document_id, aircraft_ids):
    query = "INSERT INTO aircraft_documents (aircraft_id, document_id) VALUES (%s, %s)"
    for aircraft_id in aircraft_ids:
        cursor.execute(query, (aircraft_id, document_id))
    
## Get foreign key IDs ##
def get_author_id(cursor, author):
    query = "SELECT staff_id FROM staff WHERE email = %s"
    cursor.execute(query, (author,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_subcategory_id(cursor, subcategory):
    query = "SELECT subcategory_id FROM subcategories WHERE name = %s"
    cursor.execute(query, (subcategory,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_aircraft_ids_by_names(cursor, aircraft):
    format_strings = ','.join(['%s'] * len(aircraft))
    query = f"SELECT aircraft_id FROM aircraft WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(aircraft))
    results = cursor.fetchall()
    return [row[0] for row in results]

## HELPERS ##
# Return server error as response
def server_error(e):
    return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(str(e))
        }

# Response headers
def headers():
    return {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        }

# For JSON date encoding
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)