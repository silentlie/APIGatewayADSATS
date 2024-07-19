import os
import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def get_method():
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        query = read_file("adsats_database.sql")
        cursor.execute(query,multi=True)
        if query.strip().upper().startswith("SELECT"):
            
            results = cursor.fetchall()
            print(results)
            for row in results:
                print(row)
        else:
            connection.commit()
            results = "Query executed successfully and changes committed"
            print(results)
        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps(results, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
    # Catch SQL exeption
    except Error as e:
        print(f"Error: {e._full_msg}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(e._full_msg)
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
            print("MySQL cursor is closed")
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

## HELPERS ##
# Create a connection to the DB
def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

# Read file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Response headers
def headers():
    return {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': allowed_headers
    }

# for dump datetime json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

## HELPERS ##
#===============================================================================