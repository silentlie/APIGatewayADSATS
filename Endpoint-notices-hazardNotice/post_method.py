from datetime import datetime, timedelta
import json
from mysql.connector import Error
import mysql.connector
import os


def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()

        # Insert a new notice
        notice_id = insert_and_get_notice_id(cursor, body)

        # Collate staff ID's from the receipients drop downs (staff by email, role, or aircraft)
        if 'staff' in body or 'aircraft' in body or 'roles' in body:
            staff_ids = get_staff_ids(cursor, body['staff'], body['aircraft'], body['roles'])
            insert_notification(cursor, staff_ids, notice_id)
            
            # TODO this will need to be seperated to a different 'if' as there will be two aircraft dropdowns
            aircraft_ids = get_aircraft_ids_by_names(cursor, body['aircraft'])
            insert_aircraft_notices(cursor, notice_id, aircraft_ids)

        # Get the document IDs for one or more documents selected to be linked to the notice
        if 'documents' in body:
            document_ids = get_documents_ids_by_file_names(cursor, body['documents'])
            insert_notice_documents(cursor, notice_id, document_ids)

        # If a attribute has been passed create a new Hazard_notice record
        if 'location' in body or 'description' in body or "report_type" in body or 'include_mitigation' in body:
            insert_hazard_details(cursor, body, notice_id)

        connection.commit()

        # Update successful message
        print("Database updated.")

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(notice_id)
        }
    except mysql.connector.Error as e:
        # Update failed message as an error
        print(f"Database update failed: {e}")

        # Reverting changes because of exception
        connection.rollback()

        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(str(e))
        }

    except Exception as e:
        print(f"Error: {e}")

        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(str(e))
        }

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# List of aircraft names
def get_aircraft_ids_by_names(cursor, aircrafts):
    format_strings = ','.join(['%s'] * len(aircrafts))
    query = f"SELECT aircraft_id FROM aircraft WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(aircrafts))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_author_id(cursor, author):
    query = "SELECT staff_id FROM staff WHERE email = %s"
    cursor.execute(query, (author,))
    result = cursor.fetchone()
    return result[0] if result else None

# Get list of roles
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

# Get list of documents
def get_documents_ids_by_file_names(cursor, documents):
    format_strings = ','.join(['%s'] * len(documents))
    query = f"SELECT document_id FROM documents WHERE file_name IN ({format_strings})"
    cursor.execute(query, tuple(documents))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_and_get_notice_id(cursor, body):
    subject = body["subject"]
    notice_at = body["notice_at"]
    author_id = get_author_id(cursor, body["author"])
    query = """
    INSERT INTO notices (subject, author_id, category, notice_at, deadline_at, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = [subject, author_id, "Notice to crew", notice_at, (datetime.now() + timedelta(days=30)).isoformat(), datetime.now()]
    cursor.execute(query, params)
    return cursor.lastrowid


def insert_hazard_details(cursor, body, notice_id):
    description = body['description']
    hazard_location = body['hazard_location']
    report_type = body ['report_type']
    include_mitigation = body['include_mitigation']
    mitigation_comment = body['mitigation_comment']
    likelihood = body ['likelihood']
    severity = body ['severity']
    risk_severity = body['risk_severity']
    comments = body['comments']
    additional_comments = body['additional_comments']
    query = """INSERT INTO hazard_details 
                            (notice_id
                            , description
                            , hazard_location
                            , report_type
                            , include_mitigation
                            , mitigation_comment
                            , likelihood
                            , severity
                            , risk_severity
                            , comments
                            , additional_comments)
                VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"""
    params = [notice_id, description, hazard_location, report_type,
              include_mitigation, mitigation_comment,likelihood, severity , risk_severity, comments, additional_comments ]
    cursor.execute(query, params)

def insert_notification(cursor, staff_ids, notice_id):
    query = "INSERT INTO notifications (notice_id, staff_id) VALUES (%s, %s)"
    for staff_id in staff_ids:
        cursor.execute(query, (notice_id, staff_id))

def insert_aircraft_notices(cursor, notice_id, aircraft_ids):
    query = "INSERT INTO aircraft_notices (notice_id, aircraft_id) VALUES (%s, %s)"
    for aircraft_id in aircraft_ids:
        cursor.execute(query, (notice_id, aircraft_id))

def insert_notice_documents(cursor, notice_id, document_ids):
    query = "INSERT INTO notice_documents (notice_id, document_id) VALUES (%s, %s)"
    for document_id in document_ids:
        cursor.execute(query, (notice_id, document_id))


# For JSON dump format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)
