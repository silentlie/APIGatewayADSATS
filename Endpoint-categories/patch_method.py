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
        
        category_id = body['category_id']

        if 'archived' in body :
            update_archived_value(cursor, category_id, body['archived'])
            connection.commit()

        if 'name' in body:
            update_category(cursor, body, category_id)
            connection.commit()
            
        if 'staff' in body:
            delete_staff_assignments(cursor, category_id)
            connection.commit()
            staff_ids = select_staff_ids(cursor, body['staff'])
            insert_permissions(cursor, staff_ids, category_id)
            connection.commit()


        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(category_id)
        }
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

def update_category(cursor, body, category_id):
    category = body["name"]
    
    update_query = """
        UPDATE categories
        SET name = %s
        WHERE category_id = %s
    """
    params = [category, category_id]
    cursor.execute(update_query, params)

def update_archived_value(cursor, category_id, archived):
   
    query = """
        UPDATE categories 
        SET archived = %s
        WHERE category_id = %s)
    """
    params = [archived, category_id] 
    cursor.execute(query, params)

def delete_staff_assignments(cursor, category_id):
    delete_query = """
        DELETE FROM permissions
        WHERE category_id = %s
    """
    params = [category_id]
    cursor.execute(delete_query, params)

def select_staff_ids(cursor, staff_emails):
    staff_ids = []
    for email in staff_emails:
        select_query = """
            SELECT staff_id
            FROM staff
            WHERE email = %s
        """
        cursor.execute(select_query, (email,))
        result = cursor.fetchone()
        if result:
            staff_ids.append(result[0])
    return staff_ids

def insert_permissions(cursor, staff_ids, category_id):
    insert_query = """
        INSERT INTO permissions (category_id, staff_id)
        VALUES (%s, %s)
    """
    for staff_id in staff_ids:
        params = (category_id, staff_id)
        cursor.execute(insert_query, params)



