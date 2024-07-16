from datetime import datetime, timedelta
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,POST,GET,PATCH'

def patch_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()

        # Update fields in the notice_details table

        # Check the notice_id has been passed in the body
        if 'notice_id' in body:
            cursor = connection.cursor(dictionary=True)
            update_crew_notice_details(cursor, body)

            # Complete the commit only after all transactions have been successfully excecuted
            # Commit changes to the database
            connection.commit()

            # Update successful message
            print("Database updated.")

            return {
                'statusCode': 200,
                'headers': headers(),
                'body': json.dumps(body["notice_id"])
        }

        # If notice_id does not exist return an error
        return {
                'statusCode': 400,
                'headers': headers(),
                'body': json.dumps('Missing parameter: "notice_id" not found')
        }
    
    except mysql.connector.Error as e:
        # Update failed message as an error
        print(f"Database update failed: {e}")

        # Reverting changes because of exception
        connection.rollback()
        return server_error(e)

    except Exception as e:
        print(f"Error: {e}")
        return server_error(e)

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

## Update linking table records ##
def update_crew_notice_details(cursor, body):
    notice_id = body['notice_id']
    message = body.get('message')

    update_fields = []
    params = []

    if message:
        update_fields.append("message = %s")
        params.append(message)

    if not update_fields:
        return

    update_query = f"""
        UPDATE notice_details
        SET {', '.join(update_fields)}
        WHERE notice_id = %s
    """
    params.append(notice_id)
    cursor.execute(update_query, params)

## HELPERS ##
# Response headers
def headers():
    return {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        }

# Return server error as response
def server_error(e):
    return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(str(e))
        }