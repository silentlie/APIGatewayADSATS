import mysql.connector
import os
import json
import datetime
from mysql.connector import Error

def delete_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        category_id = body["category_id"]

        if not category_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: category_id must be provided")
            }

        update_query = """
            UPDATE categories
            SET deleted_at = %s
            WHERE category_id = %s
        """

        cursor.execute(update_query, (datetime.datetime.now(), category_id))
        connection.commit()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(category_id)
        }
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

    

