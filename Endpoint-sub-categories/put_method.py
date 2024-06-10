import mysql.connector
import os
import json
from mysql.connector import Error

def put_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database"
        )
        cursor = connection.cursor()

        subcategory_id = body.get("subcategory_id")
        category = body.get("category")
        newsub_name = body.get("newsub_name")
        description = body.get("description")
        new_archived = body.get("new_archived")
        
        category_ids = []
        if category:
            category_ids = get_category_ids_by_names(cursor, category)
            connection.commit()
        
        if not category_ids:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: category does not exist")
            }

        if subcategory_id is None or not category_ids or newsub_name is None or description is None or new_archived is None:
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid input: subcategory_id, category, newsub_name, description, and new_archived must be provided")
            }

        # Convert string "true" or "false" to boolean value
        if isinstance(new_archived, str):
            if new_archived.lower() == "true":
                new_archived = True
            elif new_archived.lower() == "false":
                new_archived = False
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps("Invalid input for new_archived: must be 'true' or 'false'")
                }

        update_query = """
            UPDATE subcategories
            SET name = %s,
                description = %s,
                category_id = %s,
                archived = %s
            WHERE subcategory_id = %s
        """

        cursor.execute(update_query, (newsub_name, description, category_ids[0], new_archived, subcategory_id))
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps("Internal server error")
        }
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
        },
        'body': json.dumps("Succeed")
    }

def get_category_ids_by_names(cursor, category):
    format_strings = ','.join(['%s'] * len(category))
    query = f"SELECT category_id FROM categories WHERE name IN ({format_strings})"
    cursor.execute(query, tuple(category))
    results = cursor.fetchall()
    return [row[0] for row in results]
