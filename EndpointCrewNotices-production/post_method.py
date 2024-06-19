from datetime import datetime, timedelta
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,GET,POST,PATCH'

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )

        cursor = connection.cursor()

        # Notice will have already been created. This endpoint will pass in the notice_id via the body
        # This endpoint will create the notice_details record
        # 'Notice to crew' notices do not require any further review - this endpoint will also update the
        #   resolved field (in notices table) to 1 (true)

        if 'notice_id' in body:
            cursor = connection.cursor(dictionary=True)
            notice_id = body['notice_id']

            # If a message has been passed create a new notice_details record
            if 'message' in body:
                insert_notice_details(cursor, body, notice_id)

            # Update notice 'resolved' field to 1 (true) to confirm notifications have been sent out.
            update_resolved(cursor, notice_id)

            # Complete the commit only after all transactions have been successfully excecuted
            # Commit changes to the database
            connection.commit()

            # Print and return successful request message
            print("Database updated.")
            return {
                'statusCode': 200,
                'headers': headers(),
                'body': json.dumps(notice_id)
            }
        
        # If notice_id is not in the request body return a bad request error
        else:
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

## Insert/update table records ##
# Create linked notice_detail record
def insert_notice_details(cursor, body, notice_id):
    message = body['message']
    query = "INSERT INTO notice_details (notice_id, message) VALUES (%s, %s)"
    params = [notice_id, message]
    cursor.execute(query, params)

# Update resolved field (in Notices table) to TRUE
def update_resolved(cursor, notice_id):
    resolved = 1
    query = """
        UPDATE notices
        SET resolved = %s
        WHERE notice_id = %s
    """
    params = [resolved, notice_id]
    cursor.execute(query, params)

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
