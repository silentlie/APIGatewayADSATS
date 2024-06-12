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
        
        role_id = body['role_id']
        
        if 'archived' in body:
            update_archived_value(cursor, role_id, body['archived'])
            connection.commit()

        if 'description' in body or 'role' in body:
            update_role(cursor, body, role_id)
            connection.commit()
            
        if 'staff' in body:
            delete_staff_role(cursor, role_id)
            connection.commit()
            staff_ids = select_staff_ids(cursor, body['staff'])
            insert_staff_role(cursor, staff_ids, role_id)
            connection.commit()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(role_id)
        }
    except Error as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps({"error": str(e)})
        }
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    

def update_role(cursor, body, role_id):
    role = body.get("role", None)
    description = body.get("description", None)
    
    update_fields = []
    params = []
    
    if role is not None:
        update_fields.append("role = %s")
        params.append(role)
    if description is not None:
        update_fields.append("description = %s")
        params.append(description)
    
    if not update_fields:
        return

    update_query = f"""
        UPDATE roles
        SET {', '.join(update_fields)}
        WHERE role_id = %s
    """
    params.append(role_id)
    cursor.execute(update_query, params)
    print(f"Updated role: {role} Description: {description} ID: {role_id}")

def update_archived_value(cursor, role_id, archived):
    query = """
        UPDATE roles 
        SET archived = %s
        WHERE role_id = %s
    """
    params = [archived, role_id]
    cursor.execute(query, params)
    print(f"Updated archived status to {archived} for role ID: {role_id}")

def delete_staff_role(cursor, role_id):
    delete_query = """
        DELETE FROM staff_roles
        WHERE role_id = %s
    """
    params = [role_id]
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

def insert_staff_role(cursor, staff_ids, role_id):
    insert_query = """
        INSERT INTO staff_roles (staff_id, role_id)
        VALUES (%s, %s)
    """
    for staff_id in staff_ids:
        params = (role_id, staff_id)
        cursor.execute(insert_query, params)



