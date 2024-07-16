import mysql.connector
import os
import json
import datetime
from mysql.connector import Error

def patch_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        notice_id = body.get("notice_id")
        
        if not notice_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: notice_id must be provided")
            }
        
        # Check if at least one field to update is present in the request body
        if any(key in body for key in ['pending_comments', 'register_updated', 'review_severity', 'review_likelihood', 'review_date']):
            update_hazard_details(cursor, body, notice_id)
            connection.commit()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: No valid fields provided for update")
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

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
        },
        'body': json.dumps(notice_id)
    }

def update_hazard_details(cursor, body, notice_id):
    pending_comments = body['pending_comments']
    register_updated = body['register_updated']
    review_severity = body['review_severity']
    review_likelihood = body['review_likelihood']
    review_date = body['review_date']
    
    update_fields = []
    update_values = []
    
    if pending_comments is not None:
        update_fields.append("pending_comments = %s")
        update_values.append(pending_comments)
    if register_updated is not None:
        update_fields.append("register_updated = %s")
        update_values.append(register_updated)
    if review_severity is not None:
        update_fields.append("review_severity = %s")
        update_values.append(review_severity)
    if review_likelihood is not None:
        update_fields.append("review_likelihood = %s")
        update_values.append(review_likelihood)
    if review_date is not None:
        update_fields.append("review_date = %s")
        update_values.append(review_date)
    
    update_values.append(notice_id)
    
    update_query = f"""
        UPDATE hazard_details 
        SET {', '.join(update_fields)}
        WHERE notice_id = %s;
    """
    
    cursor.execute(update_query, tuple(update_values))
