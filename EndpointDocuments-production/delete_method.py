import datetime
import json
import os

import mysql.connector
from mysql.connector import Error

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def delete_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        document_id = body["document_id"]

        if not document_id:
            return {
                'statusCode': 400,
                'headers': headers(),
                'body': json.dumps("Invalid input: document_id must be provided")
            }

        update_query = """
            UPDATE documents
            SET deleted_at = %s
            WHERE document_id = %s
        """

        cursor.execute(update_query, (datetime.datetime.now(), document_id))
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps("Internal server error")
        }
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    return {
        'statusCode': 200,
        'headers': headers(),
        'body': json.dumps(document_id)
    }

## HELPERS ##
# Response headers
def headers():
    return {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        }
