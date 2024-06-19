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

        # Check the notice_id has been passed in the body
        if 'notice_id' in body:
            cursor = connection.cursor(dictionary=True)
            update_hazard_details(cursor, body)

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
def update_hazard_details(cursor, body):
    notice_id = body['notice_id']
    description = body.get('description')
    hazard_location = body.get('hazard_location')
    report_type = body.get('report_type')
    include_mitigation = body.get('include_mitigation')
    mitigation_comment = body.get('mitigation_comment')
    likelihood = body.get('likelihood')
    severity = body.get('severity')
    risk_severity = body.get('risk_severity')
    comments = body.get('comments')
    review_date = body.get('review_date')
    review_likelihood = body.get('review_likelihood')
    review_severity = body.get('review_severity')
    register_updated = body.get('register_updated')

    update_fields = []
    params = []

    if description:
        update_fields.append("description = %s")
        params.append(description)

    if hazard_location:
        update_fields.append("hazard_location = %s")
        params.append(hazard_location)

    if report_type:
        update_fields.append("report_type = %s")
        params.append(report_type)
        
    if include_mitigation:
        update_fields.append("include_mitigation = %s")
        params.append(include_mitigation)
        
    if mitigation_comment:
        update_fields.append("mitigation_comment = %s")
        params.append(mitigation_comment)
        
    if likelihood:
        update_fields.append("likelihood = %s")
        params.append(likelihood)
        
    if severity:
        update_fields.append("severity = %s")
        params.append(severity)
        
    if risk_severity:
        update_fields.append("risk_severity = %s")
        params.append(risk_severity)
                
    if comments:
        update_fields.append("comments = %s")
        params.append(comments)
                
    if review_date:
        update_fields.append("review_date = %s")
        params.append(review_date)
                
    if review_likelihood:
        update_fields.append("review_likelihood = %s")
        params.append(review_likelihood)
                
    if review_severity:
        update_fields.append("review_severity = %s")
        params.append(review_severity)
                
    if register_updated:
        update_fields.append("register_updated = %s")
        params.append(register_updated)

    if not update_fields:
        return

    update_query = f"""
        UPDATE hazard_details
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