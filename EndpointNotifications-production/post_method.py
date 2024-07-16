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

        # Combined staff_ids
        combined_results = []

        # Notice will have already been created. This endpoint will pass in the notice_id via the body
        # This endpoint will create the notification records and updated issued (in the notices table) to true.
        if 'notice_id' in body:
            cursor = connection.cursor(dictionary=True)
            notice_id = body['notice_id']

            # Collate staff ID's from the recipients drop downs (staff by email, role, or aircraft)
            if 'staff' in body:
                #staff_ids = get_staff_ids(cursor, body['staff'], body['aircraft'], body['roles'])
                staff_ids_from_emails = get_staff_ids_from_emails(cursor, body['staff'])
                combined_results.extend(staff_ids_from_emails)
            
            if 'aircraft' in body:
                staff_ids_from_aircraft = get_staff_ids_from_aircraft(cursor, body['aircraft'])
                combined_results.extend(staff_ids_from_aircraft)
            
            if 'roles' in body:
                staff_ids_from_roles = get_staff_ids_from_roles(cursor, body['roles'])
                combined_results.extend(staff_ids_from_roles)
            
            if 'staff' in body or 'aircraft' in body or 'roles' in body:
                # Flatten the results and convert to a set to get unique values
                distinct_results = set(combined_results)
                
                # Convert set back to a list
                staff_ids = list(distinct_results)

                # Add new notification table records as per selected recipients
                insert_notification(cursor, staff_ids, notice_id)

                # Update notice 'issued' field to 1 (true) to confirm notifications have been sent out.
                update_issued(cursor, notice_id)
            else:
                return {
                'statusCode': 400,
                'headers': headers(),
                'body': json.dumps('Missing parameter from body: Must include staff[] OR roles[] OR aircraft[]')
            }

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
                'body': json.dumps('Missing parameter from body: "notice_id" not found')
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
# Create notifications records for each staff that has been selected as a recipient
def insert_notification(cursor, staff_ids, notice_id):
    query = """
    INSERT INTO notifications 
    (notice_id, staff_id, status) 
    VALUES (%s, %s, FALSE)
    ON DUPLICATE KEY UPDATE status = FALSE, 
    read_at = NULL
    """
    for staff_id in staff_ids:
        cursor.execute(query, (notice_id, staff_id))

# Update issued (in Notices table) to TRUE
def update_issued(cursor, notice_id):
    issued = 1
    query = """
        UPDATE notices
        SET issued = %s
        WHERE notice_id = %s
    """
    params = [issued, notice_id]
    cursor.execute(query, params)

## Fetch foreign key IDs ##
# Get collated, unique list of staff_ids based on recipient selections
def get_staff_ids(cursor, staff, aircraft, roles):
    format_strings_roles = ','.join(['%s'] * len(roles))
    format_strings_aircraft = ','.join(['%s'] * len(aircraft))
    format_strings_staff = ','.join(['%s'] * len(staff))
    query = f"""
    SELECT DISTINCT s.staff_id
    FROM aircraft AS a
    INNER JOIN aircraft_staff AS ass ON a.aircraft_id = ass.aircraft_id
    INNER JOIN staff AS s ON s.staff_id = ass.staff_id
    WHERE a.name IN ({format_strings_aircraft})
    UNION
    SELECT DISTINCT s.staff_id
    FROM staff_roles AS sr
    INNER JOIN staff AS s ON s.staff_id = sr.staff_id
    INNER JOIN roles AS r ON r.role_id = sr.role_id
    WHERE r.role IN ({format_strings_roles})
    UNION
    SELECT DISTINCT staff_id
    FROM staff
    WHERE email IN ({format_strings_staff})
    """
    cursor.execute(query, tuple(aircraft + roles + staff))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_staff_ids_from_emails(cursor, staff):
    format_strings_staff = ','.join(['%s'] * len(staff))
    query = f"""
    SELECT DISTINCT staff_id
    FROM staff
    WHERE email IN ({format_strings_staff})
    """
    cursor.execute(query, tuple(staff))
    results = cursor.fetchall()
    return [row['staff_id'] for row in results]

def get_staff_ids_from_aircraft(cursor, aircraft):
    format_strings_aircraft = ','.join(['%s'] * len(aircraft))
    query = f"""
    SELECT DISTINCT s.staff_id
    FROM aircraft AS a
    INNER JOIN aircraft_staff AS ass ON a.aircraft_id = ass.aircraft_id
    INNER JOIN staff AS s ON s.staff_id = ass.staff_id
    WHERE a.name IN ({format_strings_aircraft})
    """
    cursor.execute(query, tuple(aircraft))
    results = cursor.fetchall()
    return [row['staff_id'] for row in results]

def get_staff_ids_from_roles(cursor, roles):
    format_strings_roles = ','.join(['%s'] * len(roles))
    query = f"""
    SELECT DISTINCT s.staff_id
    FROM staff_roles AS sr
    INNER JOIN staff AS s ON s.staff_id = sr.staff_id
    INNER JOIN roles AS r ON r.role_id = sr.role_id
    WHERE r.role IN ({format_strings_roles})
    """
    cursor.execute(query, tuple(roles))
    results = cursor.fetchall()
    return [row['staff_id'] for row in results]

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
