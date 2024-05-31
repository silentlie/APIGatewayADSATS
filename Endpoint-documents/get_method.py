from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os
# I've refactor the code so it look a little different
def get_method(parameters):
    try:
        # connect_to_db function is separate for easier to read
        connection = connect_to_db()
        
        # build_query function is base on method for example this take parameters
        # the method return query and parameters for binding
        query, params = build_query(parameters)
        # get total records first
        total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
        cursor = connection.cursor()
        cursor.execute(total_query, params)
        total_records = cursor.fetchone()[0] # type: ignore
        cursor = connection.cursor(dictionary=True)
        query += " LIMIT %s OFFSET %s"
        # in parameters of method number by default is a str so must convert back to int
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])
        # excute the query
        cursor.execute(query, params)
        # this is get method which return data base on parameters so cursor.fetchall is call
        # but in some method we only need to know if the query is succeed or not
        # use cursor.commit()
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
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# this is when start to build query
def build_query(parameters):
    # the base query
    query = """
    SELECT d.document_id, d.file_name, u.email AS email, d.archived, d.created_at
    , s.name AS sub_category, c.name AS category
    , GROUP_CONCAT(a.name SEPARATOR ', ') AS aircraft
    FROM documents AS d
    JOIN users AS u ON d.uploaded_by_id = u.user_id
    JOIN subcategories AS s ON s.subcategory_id = d.subcategory_id
    JOIN categories AS c ON s.category_id = c.category_id
    LEFT OUTER JOIN aircraft_documents AS ad ON ad.document_id = d.document_id
    LEFT OUTER JOIN aircrafts AS a ON ad.aircraft_id = a.aircraft_id
    """
    query += " WHERE d.deleted_at IS Null"
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # search file name in parameters of method should be "%aircraft%"
    if 'file_name' in parameters:
        filters.append("file_name LIKE %s")
        params.append(parameters["file_name"])
    # search for one or many emails/users/authors
    if 'emails' in parameters:
        emails = parameters["emails"].split(',')
        placeholders = ', '.join(['%s'] * len(emails))
        filters.append(f"email IN ({placeholders})")
        params.extend(emails)
    if 'sub_categories' in parameters:
        sub_categories = parameters["sub_categories"].split(',')
        placeholders = ', '.join(['%s'] * len(sub_categories))
        filters.append(f"sub_category IN ({placeholders})")
        params.extend(sub_categories)
    if 'categories' in parameters:
        categories = parameters["categories"].split(',')
        placeholders = ', '.join(['%s'] * len(categories))
        filters.append(f"category IN ({placeholders})")
        params.extend(categories)
    # search for one or many aircrafts that relate to document
    if 'aircrafts' in parameters:
        aircrafts = parameters["aircrafts"].split(',')
        placeholders = ', '.join(['%s'] * len(aircrafts))
        filters.append(f"aircraft IN ({placeholders})")
        params.extend(aircrafts)
    # start date and end date of create_at
    if 'create_at' in parameters:
        create_at = parameters["create_at"].split(',')
        filters.append("d.created_at BETWEEN %s AND %s")
        params.extend(create_at)
    # archived or not
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"archived = {parameters["archived"]}")
    
    # no filters for users that relate documents
    # if they want to reference go to notices
    # or create many to many table again between documents and users
    # but it's very complex to filter by users and roles
    
    # if there is any filter add base query
    if filters:
        query += " AND " + " AND ".join(filters)
    # must have because GROUP_CONCAT
    query += " GROUP BY d.document_id "
    # if doesnt provide a sort column default is pk of documents
    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        # Add other valid column names if necessary
        valid_columns = ["document_id", "file_name", "email", "archived", "created_at", "subcategory", "category", "aircrafts"]
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