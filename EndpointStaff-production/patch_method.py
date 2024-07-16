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
        
        staff_id = body.get('staff_id')
        
        if 'archived' in body:
            update_archived_value(cursor, staff_id, body['archived'])
            connection.commit()

        if 'f_name' in body or 'l_name' in body or 'email' in body:
            update_staff(cursor, body, staff_id)
            connection.commit()
            
        if 'roles' in body:
            delete_role_value(cursor, staff_id)
            connection.commit()
            role_ids = select_role_id(cursor, body['roles'])
            insert_new_roles(cursor, staff_id, role_ids)
            connection.commit()
            
        if 'aircraft' in body:
            delete_aircraft_value(cursor, staff_id)
            connection.commit()
            aircraft_ids = select_aircraft_id(cursor,body['aircraft'])
            insert_new_aircraft(cursor, staff_id, aircraft_ids )
            connection.commit()
            
        if 'categories' in body:
            delete_permission_value(cursor, staff_id)
            connection.commit()
            category_ids = select_category_id(cursor,   body['categories'])
            insert_new_permissions(cursor, staff_id, category_ids)
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
        'body': json.dumps(staff_id)
    }

def update_staff(cursor, body, staff_id):
    f_name = body["f_name"]
    l_name = body["l_name"]
    email = body["email"]

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

def delete_role_value(cursor, staff_id):
    query = """
            DELETE FROM staff_roles
            WHERE staff_id = %s
            """
    params = [staff_id]
    cursor.execute(query, params)
    
def select_role_id(cursor, roles):
    query = """
                SELECT role_id
                FROM roles
                WHERE role = %s
            """
    role_ids = []
    for role_name in roles:
        cursor.execute(query, [role_name])
        result = cursor.fetchone()  
        if result:
            role_ids.append(result[0])  
    return role_ids

def insert_new_roles(cursor, staff_id, roles):
    query = """
            INSERT INTO staff_roles (role_id, staff_id)
            VALUES (%s, %s)
            """
    for role in roles:
        params = [role, staff_id]
        cursor.execute(query, params)  

def delete_aircraft_value(cursor, staff_id):
    query = """
            DELETE FROM aircraft_staff
            WHERE staff_id = %s
            """
    params = [staff_id]
    cursor.execute(query, params)
    
def select_aircraft_id(cursor, aircraft):
    query = """
                SELECT aircraft_id
                FROM aircraft
                WHERE name = %s
            """
    aircraft_ids = []
    for name in aircraft:
        cursor.execute(query, [name])
        # name of aircrfats are unique
        result = cursor.fetchone()  
        if result:
            aircraft_ids.append(result[0])  
    return aircraft_ids
    
def insert_new_aircraft(cursor, staff_id, aircraft):
    query = """
            INSERT INTO aircraft_staff (aircraft_id, staff_id)
            VALUES (%s, %s)
            """
    for aircraft in aircraft:
        params = [aircraft, staff_id]
        cursor.execute(query, params)      

def delete_permission_value(cursor, staff_id):
    query = """
            DELETE FROM permissions
            WHERE staff_id = %s
            """
    params = [staff_id]
    cursor.execute(query, params)

def select_category_id(cursor, categories):
    query = """
                SELECT category_id
                FROM categories
                WHERE name = %s
            """
    category_ids = []
    for name in categories:
        cursor.execute(query, [name])
        result = cursor.fetchone()  
        if result:
            category_ids.append(result[0])  
    return category_ids
    
def insert_new_permissions(cursor, staff_id, categories):
    query = """
            INSERT INTO permissions (category_id, staff_id)
            VALUES (%s, %s)
            """
    for category in categories:
        params = [category, staff_id]
        cursor.execute(query, params)
