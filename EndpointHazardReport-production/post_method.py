from datetime import datetime, timedelta
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,POST,GET,PATCH'

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
        # 'Hazard notices' require further review so resolved will be left as 0

        # Check the notice_id has been passed in the body
        if 'notice_id' in body:
            cursor = connection.cursor(dictionary=True)
            insert_hazard_details(cursor, body)

            # Complete the commit only after all transactions have been successfully excecuted
            # Commit changes to the database
            connection.commit()

            # Update successful message
            print("Database updated.")

            return {
                'statusCode': 200,
                'headers': headers(),
                'body': json.dumps(f"Success: notice details have been added for notice ID: {body["notice_id"]})")
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

## Insert linking table records ##
def insert_hazard_details(cursor, body):
    notice_id = body['notice_id']
    description = body.get('description', None)
    hazard_location = body.get('hazard_location', None)
    report_type = body.get('report_type', None)
    include_mitigation = body.get('include_mitigation', None)
    mitigation_comment = body.get('mitigation_comment', None)
    likelihood = body.get('likelihood', None)
    severity = body.get('severity', None)
    risk_severity = body.get('risk_severity', None)
    comments = body.get('comments', None)

    # SQL query
    query = """
    INSERT INTO hazard_details 
        (notice_id,
        description,
        hazard_location,
        report_type,
        include_mitigation,
        mitigation_comment,
        likelihood,
        severity,
        risk_severity,
        comments)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [notice_id, description, hazard_location, report_type, include_mitigation, 
               mitigation_comment, likelihood, severity, risk_severity, comments]
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