import mysql.connector
import os
import json
from mysql.connector import Error

def patch_method(body):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()
        
        staff_id = body['staff_id']
        
        if 'archived' in body:
            update_archived_value(cursor, staff_id, body['archived'])
            connection.commit()

        if 'f_name' in body or 'l_name' in body or 'email' in body:
            update_staff(cursor, body, staff_id)
            connection.commit()

    except Error as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
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
        'body': json.dumps("Succeeded")
    }

def update_staff(cursor, body, staff_id):
    f_name = body.get("f_name")
    l_name = body.get("l_name")
    email = body.get("email")

    update_query = """
        UPDATE staff
        SET f_name = %s,
            l_name = %s,
            email = %s
        WHERE staff_id = %s
    """
    params = [f_name, l_name, email, staff_id]
    cursor.execute(update_query, params)

def update_archived_value(cursor, staff_id, archived):
    query = """
        UPDATE staff 
        SET archived = %s
        WHERE staff_id = %s
    """
    params = [archived, staff_id]
    cursor.execute(query, params)
