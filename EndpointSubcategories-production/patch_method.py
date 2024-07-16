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
        
        subcategory_id = body['subcategory_id']

        if 'archived' in body:
            update_archived_value(cursor, subcategory_id, body['archived'])
            connection.commit()

        if 'name' in body or 'description' in body or 'category' in body:
            update_subcategory(cursor, body, subcategory_id)
            connection.commit()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(subcategory_id)
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

    

def update_subcategory(cursor, body, subcategory_id):
    subcategory = body.get("name", None)
    catgeory = body.get("category", None)
    description = body.get("description",None)
    
    category_id = get_category_id(cursor, catgeory)
    
    update_query = """
        UPDATE subcategories
        SET
            category_id = %s,
            name= %s,
            description = %s
        WHERE subcategory_id = %s
    """
    params = [category_id, subcategory,description, subcategory_id]
    cursor.execute(update_query, params)

def update_archived_value(cursor, subcategory_id, archived):
    
    query = """
        UPDATE subcategories 
        SET archived = %s
        WHERE subcategory_id = %s
    """
    params = [archived, subcategory_id]
    cursor.execute(query, params)

def get_category_id(cursor, catgeory):
    query = "SELECT category_id FROM categories WHERE name = %s"
    cursor.execute(query, (catgeory,))
    result = cursor.fetchone()
    return result[0]

