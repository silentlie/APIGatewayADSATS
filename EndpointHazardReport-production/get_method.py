from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,POST,GET,PATCH'

def get_method(parameters):
    connection = None
    cursor = None
    try:
        connection = connect_to_db()
        
        if 'notice_id' in parameters:
            cursor = connection.cursor(dictionary=True)
            return get_specific_notice(cursor, parameters)

        return {
            'statusCode': 400,
            'headers': headers(),
            'body': json.dumps('Missing parameter: "id" not found', indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {str(e)}")
        
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(str(e))
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def get_specific_notice(cursor, parameters):
    try:
        query = """
                SELECT 
                    *
                FROM hazard_details
                WHERE notice_id = %s 
                """
        params = [parameters["id"]]
        cursor.execute(query, params)
        rows = cursor.fetchall()
        print(f"Query successful, rows fetched: {len(rows)}")
        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(rows, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
    except Error as e:
        print(f"Error executing query: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(str(e))
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