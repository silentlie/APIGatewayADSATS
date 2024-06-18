from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    connection = None
    cursor = None
    try:
        connection = connect_to_db()
        
        if 'id' in parameters:
            cursor = connection.cursor(dictionary=True)
            return get_specific_notice(cursor, parameters)

        return {
            'statusCode': 400,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps('Missing parameter: "id" not found', indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {str(e)}")
        
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(str(e))
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        print("Database connection established")
        return connection
    except Error as e:
        print(f"Error connecting to database: {str(e)}")
        raise

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def get_specific_notice(cursor, parameters):
    try:
        query = """
                SELECT 
                    n.notice_id,
                    u.email AS author,
                    n.subject,
                    n.notice_at,
                    n.deadline_at,
                    hd.description,
                    hd.hazard_location,
                    hd.report_type,
                    hd.include_mitigation,
                    hd.mitigation_comment,
                    hd.likelihood,
                    hd.severity,
                    hd.comments,
                    hd.additional_comments,
                    hd.register_updated,
                    hd.pending_comments
                FROM notices AS n
                JOIN staff AS u ON u.staff_id = n.author_id
                INNER JOIN hazard_details AS hd ON n.notice_id = hd.notice_id
                WHERE n.notice_id = %s 
                """
        params = [parameters["id"]]
        cursor.execute(query, params)
        rows = cursor.fetchall()
        print(f"Query successful, rows fetched: {len(rows)}")
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
        print(f"Error executing query: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(str(e))
        }
