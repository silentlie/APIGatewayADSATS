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

        # Update fields in the hazard_details table

        # Get the staff_id from the email
        if 'email' in body:
            cursor = connection.cursor(dictionary=True)
            author_id = get_staff_id_from_email(cursor, body)

        # Check the notice_id has been passed in the body
        if 'notice_id' in body:
            cursor = connection.cursor(dictionary=True)
            update_notice_details(cursor, body, author_id)

            # Complete the commit only after all transactions have been successfully excecuted
            # Commit changes to the database
            connection.commit()

            # Update successful message
            print("Database updated.")

            return {
                'statusCode': 200,
                'headers': headers(),
                'body': json.dumps(f"Success: notice has been sent (notice ID: {body["notice_id"]})")
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
def update_notice_details(cursor, body, author_id):
    notice_id = body['notice_id']
    email = body.get('email')
    category = body.get('category')
    subject = body.get('subject')
    resolved = body.get('resolved')
    issued = body.get('issued')
    lodged = body.get('lodged')
    notice_at = body.get('notice_at')
    deadline_at = body.get('deadline_at')
    deleted_at = body.get('deleted_at')
    archived = body.get('archived')
    pending_reason = body.get('pending_reason')
    additional_comments = body.get('additional_comments')

    update_fields = []
    params = []

    if email:
        update_fields.append("author_id = %s")
        params.append(author_id)

    if category:
        update_fields.append("category = %s")
        params.append(category)

    if subject:
        update_fields.append("subject = %s")
        params.append(subject)

    if resolved:
        update_fields.append("resolved = %s")
        params.append(resolved)
        
    if issued:
        update_fields.append("issued = %s")
        params.append(issued)
        
    if lodged:
        update_fields.append("lodged = %s")
        params.append(lodged)
        
    if notice_at:
        update_fields.append("notice_at = %s")
        params.append(notice_at)
        
    if deadline_at:
        update_fields.append("deadline_at = %s")
        params.append(deadline_at)
        
    if deleted_at:
        update_fields.append("deleted_at = %s")
        params.append(deleted_at)
                
    if archived:
        update_fields.append("archived = %s")
        params.append(archived)
                
    if pending_reason:
        update_fields.append("pending_reason = %s")
        params.append(pending_reason)
                
    if additional_comments:
        update_fields.append("additional_comments = %s")
        params.append(additional_comments)

    if not update_fields:
        return

    update_query = f"""
        UPDATE notices
        SET {', '.join(update_fields)}
        WHERE notice_id = %s
    """
    params.append(notice_id)
    cursor.execute(update_query, params)

## 
def get_staff_id_from_email(cursor, body):
    email = body['email']
    query = "SELECT staff_id FROM staff WHERE email IN %s"
    params = [email]
    cursor.execute(query, params)
    return cursor.fetchone()[0]


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