from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,GET,POST'

# Endpoint > /notices/notice-to-crew
# This will get a single notice record based on the 'id' parameter to return
# to the user showing the full details of the notice they have selected from the table.

def get_method(parameters):
    try:
        connection = connect_to_db()
        
        if 'id' in parameters:
            cursor = connection.cursor(dictionary=True)
            return get_specific_notice(cursor, parameters)

        return {
            'statusCode': 400,
            'headers': headers(),
            'body': json.dumps('Missing parameter: "id" not found', indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {e._full_msg}")
        
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(e._full_msg)
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def get_specific_notice(cursor, parameters):
    
    query = """
            SELECT 
                n.notice_id,
                u.email AS author,
                n.subject,
                nd.message,
                n.notice_at,
                n.deadline_at,
                n.issued,
                n.resolved
            FROM notices AS n
            JOIN notice_details AS nd ON nd.notice_id = n.notice_id
            JOIN staff AS u ON u.staff_id = n.author_id
            WHERE n.notice_id = %s 
            """
    params= [parameters["id"]]
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return {
        'statusCode': 200,
        'headers': headers(),
        'body': json.dumps(rows, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
    }

## HELPERS ##
# create a connect to db
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

# for dump json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
# ===========================================================================