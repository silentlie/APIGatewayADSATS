import json
from mysql.connector import Error
import mysql.connector
import os
from datetime import datetime

def post_method(body):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()
        subcategory_name = body["subcategory_name"]
        check_query = "SELECT COUNT(*) FROM subcategories WHERE subcategory_name = %s"
        cursor.execute(check_query, (subcategory_name,))
        result = cursor.fetchone()

        if result[0] > 0: # type: ignore
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
                'body': json.dumps(f"subcategory with name '{subcategory_name}' already exists.")
            }
        subcategory_id = insert_and_get_subcategory_id(cursor, body)
        connection.commit()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps(subcategory_id, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
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
            'body': json.dumps(str(e))
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def insert_and_get_subcategory_id(cursor, body):
    category_name = body["category_name"]
    subcategory_name = body["subcategory_name"]
    description = body["description"]
    
    category_id = get_category_id(cursor, category_name)
        
    query = """
    INSERT INTO subcategories (category_id, name, description, archived)
    VALUES (%s, %s, %s, %s)
    """
    params = [category_id, subcategory_name, description, False]
    cursor.execute(query, params)
    
    query = "SELECT subcategory_id FROM subcategories WHERE name = %s"
    cursor.execute(query, (subcategory_name,))
    result = cursor.fetchone()
    print(result)
    return result[0]

def get_category_id(cursor, category_name):
    select_category_id = """SELECT category_id FROM categories WHERE name = %s"""
    cursor.execute(select_category_id, (category_name,))
    category_id = cursor.fetchone()
    if category_id is not None:
        return category_id[0]
    else:
        # Handle case where category is not found
        return None

# for dump json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
