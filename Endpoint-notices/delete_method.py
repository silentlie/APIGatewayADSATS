import mysql.connector
import os
import json
import datetime
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

        notice_id = body["notice_id"]

        if not notice_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: notice_id must be provided")
            }

        update_query = """
            UPDATE notices 
            SET deleted_at = %s
            WHERE notice_id = %s;
        """

        cursor.execute(update_query, (datetime.datetime.now(), notice_id))
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
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
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        },
        'body': json.dumps(notice_id)
    }


