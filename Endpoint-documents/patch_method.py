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
        document_id = body['document_id']
        if 'archived' in body:
            update_archived_value(cursor, document_id, body['archived'])
            connection.commit()

        if 'email' in body or 'subcategory' in body or 'file_name' in body:
            update_document(cursor, body, document_id)
            connection.commit()
            
        if 'aircraft' in body:
            delete_aircraft_document(cursor, document_id)
            connection.commit()
            aircraft_ids = select_aircraft_ids(cursor, body['aircraft'])
            insert_aircraft_document(cursor, document_id, aircraft_ids)
            connection.commit()

    except Error as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
        },
        'body': json.dumps(document_id)
    }

def update_document(cursor, body, document_id):
    file_name = body["file_name"]
    email = body["email"]
    subcategory = body["subcategory"]
    
    subcategory_id = get_subcategory_id(cursor, subcategory)
    staff_id = get_staff_id(cursor, email)
    
    update_query = """
        UPDATE documents
        SET
            author_id = %s,
            subcategory_id = %s,
            file_name = %s
        WHERE document_id = %s
    """
    params = [staff_id, subcategory_id, file_name, document_id]
    cursor.execute(update_query, params)

def update_archived_value(cursor, document_id, archived):

    query = """
        UPDATE documents 
        SET archived = %s
        WHERE document_id = %s
    """
    params = [archived , document_id] 
    cursor.execute(query, params)

def get_subcategory_id(cursor, subcategory):
    query = "SELECT subcategory_id FROM subcategories WHERE name = %s"
    cursor.execute(query, (subcategory,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_staff_id(cursor, email):
    query = "SELECT staff_id FROM staff WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    return result[0] if result else None

def delete_aircraft_document(cursor, document_id):
    delete_query = """ DELETE FROM aircraft_documents
                         WHERE document_id = %s
                        """
    params = [document_id]
    cursor.execute(delete_query, params)
    
def select_aircraft_ids(cursor, aircraft):
    aircraft_id = []
    for name in aircraft:
        select_query = """
            SELECT aircraft_id
            FROM aircraft
            WHERE name = %s
        """
        cursor.execute(select_query, (name,))
        result = cursor.fetchone()
        if result:
            aircraft_id.append(result[0])
    return aircraft_id


def insert_aircraft_document(cursor, document_id, aircraft_ids):
    insert_query = """
        INSERT INTO aircraft_documents (document_id, aircraft_id)
        VALUES (%s, %s)
    """
    for id in aircraft_ids:
        params = (document_id, id)
        cursor.execute(insert_query, params)