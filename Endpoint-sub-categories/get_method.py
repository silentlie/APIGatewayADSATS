from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    if not parameters:
        return get_method_no_parameters()
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
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(response, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {e._full_msg}")
        
        return {
            'statusCode': 500,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(e._full_msg)
        }

# this is when start to build query
def build_query(parameters):
    # the base query
    query = """
    SELECT 
        s.subcategory_id,
        s.name,
        s.description,
        s.archived,
        c.name AS category
    FROM `subcategories` AS s
    JOIN categories AS c
    WHERE s.deleted_at IS Null
    """
    
    filters = []
    params = []
    # search for name of category
    if 'name' in parameters:
        filters.append("s.name LIKE %s")
        params.append(parameters["name"])
    
    # filter based on archived or not
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"s.archived = {parameters["archived"]}")
    
    # if there is any filter add base query
    if filters:
        query += " AND " + " AND ".join(filters)
    # # must have because GROUP_CONCAT
    # query += " GROUP BY d.document_id "
    # if doesnt provide a sort column default is pk of documents
    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        # Add other valid column names if necessary
        valid_columns = ["subcategory_id", "name", "description", "archived", "category"]
        if parameters["sort_column"] in valid_columns:
            # asc if true, desk if false
            order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
            # in this part must parse as str cannot use binding because sort_column cannot be str
            query += f" ORDER BY {parameters["sort_column"]} {order}"
    
    # finish prepare query and params
    print(query)
    print(params)
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
    
# return a list string for filtering, searching, sending
def get_method_no_parameters():
    try:
        # get all of subcategories names where it is not archived
        query = "SELECT name from subcategories"
        query += " WHERE archived = false"
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query)
        response = cursor.fetchall() 
        subcategories = [item[0] for item in response] # type: ignore
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(subcategories, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
    except Error as e:
        print(f"Error: {e._full_msg}")
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
                },
            'body': json.dumps(e._full_msg)
        }
    