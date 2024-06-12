import mysql.connector
import os
import json
from mysql.connector import Error

def put_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        role_id = body["role_id"]
        new_role = body["new_role"]
        new_description = body["new_description"]
        new_archived = body["new_archived"]

        if new_role is None or new_archived is None or role_id is None:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: role_id, new_role, and new_archived must be provided")
            }

        # Convert string "true" or "false" to boolean value
        if isinstance(new_archived, str):
            if new_archived.lower() == "true":
                new_archived = True
            elif new_archived.lower() == "false":
                new_archived = False
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps("Invalid input for new_archived: must be 'true' or 'false'")
                }

        update_query = """
            UPDATE roles
            SET role = %s,
                description = %s,
                archived = %s
            WHERE role_id = %s
        """

        cursor.execute(update_query, (new_role, new_description, new_archived, role_id))
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps("Internal server error")
        }
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
        },
        'body': json.dumps("Succeed")
    }
