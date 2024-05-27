import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        query, params = build_query(parameters)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        response = []
        for row in results:
            response.append(row)
            print(row)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
        'body': json.dumps(response, indent=4, separators=(',', ':'))
    }

def build_query(parameters):
    query = """
    SELECT d.document_id, d.file_name, u.email, d.archived, d.created_at, d.modified_at, ss.name, GROUP_CONCAT(a.name SEPARATOR ', ') 
    FROM documents AS d
    JOIN users AS u ON d.uploaded_by_id = u.user_id
    JOIN subcategories AS ss ON ss.subcategory_id = d.subcategory_id
    JOIN aircraft_documents AS ad ON ad.documents_id = d.document_id
    JOIN aircrafts AS a ON ad.aircrafts_id = a.aircraft_id
    """

    filters = []
    params = []
    
    if 'name' in parameters:
        filters.append("d.file_name = %s")
        params.append(parameters["name"])
    
    if 'emails' in parameters:
        emails = parameters["emails"].split(',')
        placeholders = ', '.join(['%s'] * len(emails))
        filters.append(f"u.email IN ({placeholders})")
        params.extend(emails)
    
    if 'timeRange' in parameters:
        time_range = parameters["timeRange"].split(',')
        filters.append("d.created_at BETWEEN %s AND %s")
        params.extend(time_range)
    
    if 'archived' in parameters:
        filters.append("d.archived = %s")
        params.append(parameters["archived"])
    
    if 'aircrafts' in parameters:
        aircrafts = parameters["aircrafts"].split(',')
        placeholders = ', '.join(['%s'] * len(aircrafts))
        filters.append(f"ad.aircraft_id IN ({placeholders})")
        params.extend(aircrafts)
    
    if filters:
        query += " WHERE " + " AND ".join(filters)
    
    if 'columnName' in parameters:
        order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
        query += f" ORDER BY d.{parameters["columnName"]} {order}"
    
    query += " LIMIT %s OFFSET %s"
    limit = parameters["limit"]
    offset = parameters["offset"]
    params.extend([limit, offset])
    return query, params

def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )