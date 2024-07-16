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

        staff_id = body["staff_id"]
        updatef_name = body["updatef_name"]
        updatel_name = body["updatel_name"]
        update_email = body["update_email"]
        new_archived = body["new_archived"]

        if staff_id is None or updatef_name is None or updatel_name is None or update_email is None or new_archived is None:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: staff_id, updatef_name, updatel_name, update_email, and new_archived must be provided")
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
            UPDATE staff
            SET f_name = %s,
                l_name = %s,
                email = %s,
                archived = %s
            WHERE staff_id = %s
        """

        cursor.execute(update_query, (updatef_name, updatel_name, update_email, new_archived, staff_id))
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
