from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
   
    error_message = ""
    try:
       
        connection = connect_to_db()
        
        query, params = build_query(parameters)
      
        total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
        cursor = connection.cursor()
        cursor.execute(total_query, params)
        total_records = cursor.fetchone()[0] # type: ignore
        cursor = connection.cursor(dictionary=True)
        
        query += " LIMIT %s OFFSET %s"
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])
      
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        response = {
            "total_records": total_records,
            "rows": rows
        }
    
    except Error as e:
        print(f"Error: {e._full_msg}")
        error_message = e._full_msg
    finally:
        
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
   
    if error_message:
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(error_message)
        }
   
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
        'body': json.dumps(response, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
    }

# this is when start to build query
def build_query(parameters):
    # the base query
    query = """
    SELECT
        c.name AS category_name,
        subcategory_id AS sub_id
        , s.name AS subcategory_name
        , s.description AS description
        , c.category_id AS category_id
    -- , c.archived AS subcategory
    -- , s.archived AS category
    FROM categories AS c
    JOIN subcategories AS s ON s.category_id = c.category_id
    """
    
    filters = []
    params = []
    if 'category_name' in parameters:
        categories = parameters["c.name"].split(',')
        placeholders_category = ', '.join(['%s'] * len(categories))
        filters.append(f"ad.aircraft_id IN ({placeholders_category})")
        params.extend(categories)
    # search for one or many emails/users/authors
    if 'subcategory_name' in parameters:
        subcategories = parameters["s.name"].split(',')
        placeholders_sub = ', '.join(['%s'] * len(subcategories))
        filters.append(f"ad.aircraft_id IN ({placeholders_sub})")
        params.extend(subcategories)
        
    
    # archived or not
    # if 'archived' in parameters:
    #     filters.append("s.archived = %s")
    #     params.append(parameters["archived"])
    
    # archived or not
    # if 'archived' in parameters:
    #     filters.append("c.archived = %s")
    #     params.append(parameters["archived"])
    # search for one or many aircrafts that relate to document
    
    
    # if there is any filter add base query
    if filters:
        query += " WHERE " + " AND ".join(filters)
    # # must have because GROUP_CONCAT
    # query += " GROUP BY d.document_id "
    # if doesnt provide a sort column default is pk of documents
    if 'sort_column' in parameters:
        # asc if true, desk if false
        order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
        # in thid part must parse as str cannot use binding because sort_column cannot be str
        query += f" ORDER BY d.{parameters["sort_column"]} {order}"
    
    # finish prepare query and params
    return query, params

# create a connect to db
def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)