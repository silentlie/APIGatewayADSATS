import json
from mysql.connector import Error
import mysql.connector
import os
from datetime import datetime

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()
        document_id = insert_and_get_document_id(cursor, body)
        connection.commit()

        # aircraft_document
        if 'aircrafts' in body:
            aircraft_ids = get_aircraft_ids_by_names(cursor, body['aircrafts'])
            insert_aircraft_document(cursor, document_id, aircraft_ids)
            connection.commit()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(document_id)
        }

    except Error as e:
        print(f"Error: {e}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(f"Error: {e}")
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def insert_and_get_document_id(cursor, body):
    file_name = body["file_name"]
    email = body["email"]
    sub_category = body["subcategory"]
    created_at = datetime.now()
    archived = body["archived"]

    select_id = """SELECT staff_id FROM staff WHERE email = %s"""
    cursor.execute(select_id, (email,))
    author_id = cursor.fetchone()
    
    if not author_id:
        raise ValueError(f"No staff found with email {email}")
    author_id = author_id[0]

    sub_category_id_query = """SELECT subcategory_id FROM subcategories WHERE name = %s"""  
    cursor.execute(sub_category_id_query, (sub_category,))
    sub_category_id = cursor.fetchone()
    
    if not sub_category_id:
        raise ValueError(f"No subcategory found with name {sub_category}")
    sub_category_id = sub_category_id[0]

    query = """
        INSERT INTO documents 
            (author_id, subcategory_id, file_name, archived, created_at, deleted_at)
        VALUES (%s, %s, %s, %s, %s, NULL)
    """
    params = [author_id, sub_category_id, file_name, archived, created_at]
    cursor.execute(query, params)
    
    cursor.execute("SELECT document_id FROM documents WHERE file_name = %s AND deleted_at IS Null", (file_name,))
    result = cursor.fetchone()
    return result[0]

def get_aircraft_ids_by_names(cursor, aircrafts):
    format_strings = ','.join(['%s'] * len(aircrafts))
    query = f"SELECT aircraft_id FROM aircrafts WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(aircrafts))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_aircraft_document(cursor, document_id, aircraft_ids):
    query = "INSERT INTO aircraft_documents (aircraft_id, document_id) VALUES (%s, %s)"
    for aircraft_id in aircraft_ids:
        cursor.execute(query, (aircraft_id, document_id))

# For JSON date encoding
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
