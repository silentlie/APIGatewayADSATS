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

        role_id = body.get("role_id")
        if role_id != 1 and role_id !=2 :
            return {
                'statusCode': 409,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
                'body': json.dumps({"error": "Action not authorised "})
            }

        if not role_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: role_id must be provided")
            }

        update_query = """
            UPDATE roles
            SET deleted_at = %s
            WHERE role_id = %s
        """

        cursor.execute(update_query, (datetime.datetime.now(), role_id))
        connection.commit()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(role_id)
        }
    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps("Internal server error")
        }
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    


