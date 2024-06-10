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
