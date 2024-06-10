from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    try:
        connection = connect_to_db()
        query, params = build_query(parameters)
        cursor = connection.cursor(dictionary=True)
        query += " LIMIT %s OFFSET %s"
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(rows, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {e._full_msg}")
        
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(e._full_msg)
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def build_query(parameters):
    query = """
        SELECT
        	n.notice_id,
            n.subject,
            u.email,
            nf.status AS status,
            nf.read_at
        FROM notices AS n
       	JOIN notifications AS nf 
        ON nf.notice_id = n.notice_id
        JOIN users AS u
        ON u.staff_id = n.author_id
    """
    query += " WHERE u.staff_id = %s "
    query += " AND n.delete_at IS Null"
    query += " AND n.archived = false"
    params = [parameters["staff_id"]]

    # finish prepare query and params
    print(query)
    print(params)
    return query, params

def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
