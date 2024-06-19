from datetime import datetime, timedelta
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()

        # Insert a new notice and set notice_id
        notice_id = insert_and_get_notice_id(cursor, body)

        # Create linking tables for documents, aircraft, 
        # Notifications will be created seperately using /notifications endpoint, notice_details or hazard_details
        #   will also be added seperately via specific endpoints for each notice type.

        # Collate aircraft ID from the Link aircraft drop down
        # TODO A seperate aircraft dropdown needs to be added to each notice to link a notice with an aircraft
        if 'aircraft' in body:
            aircraft_ids = get_aircraft_ids_by_names(cursor, body['aircraft'])
            insert_aircraft_notices(cursor, notice_id, aircraft_ids)

        # Get the document IDs for one or more documents selected to be linked to the notice
        if 'documents' in body:
            document_ids = get_documents_ids_by_file_names(cursor, body['file_names'])
            insert_notice_documents(cursor, notice_id, document_ids)

        # Complete the commit only after all transactions have been successfully excecuted
        # Commit changes to the database
        connection.commit()

        # Update successful message
        print("Database updated.")

        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(notice_id)
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


# Insert a new notice and return the notice ID
def insert_and_get_notice_id(cursor, body):
    subject = body["subject"]
    notice_at = body["notice_at"] if 'notice_at' in body else datetime.now()
    category = body["category"]
    author_id = get_author_id(cursor, body["author"])
    deadline_at = body["deadline_at"] if 'deadline_at' in body else (datetime.now() + timedelta(days=30)).isoformat()
    
    # SQL query
    query = """
    INSERT INTO notices (subject, author_id, category, notice_at, deadline_at, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = [subject, author_id, category, notice_at, deadline_at, datetime.now()]
    cursor.execute(query, params)
    return cursor.lastrowid

## Insert linking table records ##
def insert_aircraft_notices(cursor, notice_id, aircraft_ids):
    query = "INSERT INTO aircraft_notices (notice_id, aircraft_id) VALUES (%s, %s)"
    for aircraft_id in aircraft_ids:
        cursor.execute(query, (notice_id, aircraft_id))

def insert_notice_documents(cursor, notice_id, document_ids):
    query = "INSERT INTO notice_documents (notice_id, document_id) VALUES (%s, %s)"
    for document_id in document_ids:
        cursor.execute(query, (notice_id, document_id))

## Fetch foreign key IDs ##
def get_author_id(cursor, author):
    query = "SELECT staff_id FROM staff WHERE email = %s"
    cursor.execute(query, (author,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_aircraft_ids_by_names(cursor, aircrafts):
    format_strings = ','.join(['%s'] * len(aircrafts))
    query = f"SELECT aircraft_id FROM aircraft WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(aircrafts))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_documents_ids_by_file_names(cursor, documents):
    format_strings = ','.join(['%s'] * len(documents))
    query = f"SELECT document_id FROM documents WHERE file_name IN ({format_strings})"
    cursor.execute(query, tuple(documents))
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