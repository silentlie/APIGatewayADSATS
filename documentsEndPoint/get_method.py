from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    error_message = ""
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        query, params = build_query(parameters)
        total_records = get_total_records(query, params, cursor)
        cursor.execute(query, params)
        results = cursor.fetchall()
        rows = []
        for row in results:
            rows.append(row)
            print(row)
        response = {
            "total_records": total_records,
            "rows": json.dumps(rows, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
    except Error as e:
        print(f"Error: {e._full_msg}")
        error_message = e._full_msg
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    if error_message:
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(error_message)
        }
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
        'body': response
    }

def build_query(parameters):
    query = """
    SELECT d.document_id, d.file_name, u.email, d.archived, d.created_at, d.modified_at, s.name AS subcategory, c.name AS category
    , GROUP_CONCAT(a.name SEPARATOR ', ') AS aircrafts
    FROM documents AS d
    JOIN users AS u ON d.uploaded_by_id = u.user_id
    JOIN subcategories AS s ON s.subcategory_id = d.subcategory_id
    JOIN categories AS c ON s.category_id = c.category_id
    LEFT OUTER JOIN aircraft_documents AS ad ON ad.documents_id = d.document_id
    LEFT OUTER JOIN aircrafts AS a ON ad.aircrafts_id = a.aircraft_id
    """

    filters = []
    params = []
    
    if 'name' in parameters:
        filters.append("d.file_name LIKE %s")
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
    
    query += " GROUP BY d.document_id "

    if 'columnName' in parameters:
        order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
        query += f" ORDER BY d.{parameters["columnName"]} {order}"
    
    query += " LIMIT %s OFFSET %s"
    limit = int(parameters["limit"])
    offset = int(parameters["offset"])
    params.extend([limit, offset])
    return query, params

def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

def get_total_records(query, params, cursor):
    total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    return result[0]

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)