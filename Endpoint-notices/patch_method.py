import mysql.connector
import os
import json
from mysql.connector import Error

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def patch_method(body):
    connection = None
    cursor = None
    try:
        # Validate input
        notice_id = body.get('notice_id')
        if not notice_id:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid input: notice_id must be provided"})
            }

        # Establish connection
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        # Update archived status if provided
        if 'archived' in body:
            update_archived_value(cursor, notice_id, body['archived'])

        # Update notice details if provided
        if 'staff' in body or 'category' in body or 'subject' in body:
            update_notice(cursor, body, notice_id)

        # Complete the commit only after all transactions have been successfully excecuted
        # Commit changes to the database
        connection.commit()

        # Update successful message
        print("Database updated.")

        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps({"notice_id": notice_id})
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

def update_notice(cursor, body, notice_id):
    category = body.get('category')
    subject = body.get('subject')
    staff = body.get('staff')

    update_fields = []
    params = []

    if category:
        update_fields.append("category = %s")
        params.append(category)

    if subject:
        update_fields.append("subject = %s")
        params.append(subject)

    if staff:
        query = """SELECT staff_id FROM staff WHERE email = %s"""
        cursor.execute(query, (staff,))
        author_id = cursor.fetchone()
        if author_id:
            update_fields.append("author_id = %s")
            params.append(author_id[0])

    if not update_fields:
        return

    update_query = f"""
        UPDATE notices
        SET {', '.join(update_fields)}
        WHERE notice_id = %s
    """
    params.append(notice_id)
    cursor.execute(update_query, params)

def update_archived_value(cursor, notice_id, archived):
    query = """
        UPDATE notices 
        SET archived = %s
        WHERE notice_id = %s
    """
    params = [archived, notice_id]
    cursor.execute(query, params)
    print(f"Updated archived status to {archived} for notice ID: {notice_id}")

## HELPERS ##
# Return server error as response
def server_error(e):
    return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(str(e))
        }

# Response headers
def headers():
    return {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        }
