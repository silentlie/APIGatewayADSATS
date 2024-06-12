import mysql.connector
import os
import json
from mysql.connector import Error

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        # Check if the category name already exists
        category_name = body["category_name"]
        check_query = "SELECT COUNT(*) FROM categories WHERE name = %s"
        cursor.execute(check_query, (category_name,))
        result = cursor.fetchone()

        if result[0] > 0: # type: ignore
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
                'body': json.dumps(f"Category with name '{category_name}' already exists.")
            }

        # Insert category and get category_id
        category_id = insert_get_category_id(cursor, body)
        connection.commit()

        # Insert into permission table
        if 'staff' in body:
            staff_ids = get_staff_ids_by_email(cursor, body['staff'])
            insert_permission(cursor, category_id, staff_ids)
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
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(f"Error: {e}")
        }
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_get_category_id(cursor, body):
    category_name = body["category_name"]
    
    query = """
        INSERT INTO categories (name, archived)
        VALUES (%s, %s)
    """
    params = [category_name, False]
    cursor.execute(query, params)

    query = "SELECT category_id FROM categories WHERE name = %s"
    cursor.execute(query, (category_name,))
    result = cursor.fetchone()
    return result[0]

def get_staff_ids_by_email(cursor, staff_email):
    format_strings = ','.join(['%s'] * len(staff_email))
    query = f"SELECT staff_id FROM staff WHERE email IN ({format_strings})"
    cursor.execute(query, tuple(staff_email))
    results = cursor.fetchall()
    return [row[0] for row in results]

def insert_permission(cursor, category_id, staff_ids):
    query = "INSERT INTO permissions (category_id, staff_id) VALUES (%s, %s)"
    for staff_id in staff_ids:
        cursor.execute(query, (category_id, staff_id))
