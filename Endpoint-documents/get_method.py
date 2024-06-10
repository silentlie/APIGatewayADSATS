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
        # nested query with limit based on staff
        nested_query, params = limit_query(parameters)
        query, params = build_query(nested_query, params, parameters)
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
def build_query(nested_query, params, parameters):
    # the base query
    query = f"""
        SELECT *
        FROM ({nested_query}) AS subquery
    """
    # define filters if any
    filters = []
    # search file name in parameters of method should be "%aircraft%"
    if 'search' in parameters:
        filters.append("file_name LIKE %s")
        params.append(parameters["search"])
    # search for one or many emails/users/authors/staff
    if 'authors' in parameters:
        authors = parameters["authors"].split(',')
        placeholders = ', '.join(['%s'] * len(authors))
        filters.append(f"author IN ({placeholders})")
        params.extend(authors)
    if 'roles' in parameters:
        roles = parameters["roles"].split(',')
        placeholders = " OR ".join(["FIND_IN_SET(%s, roles) > 0"] * len(roles))
        filters.append(f"({placeholders})")
        params.extend(roles)
    if 'subcategories' in parameters:
        sub_categories = parameters["subcategories"].split(',')
        placeholders = ', '.join(['%s'] * len(sub_categories))
        filters.append(f"subcategory IN ({placeholders})")
        params.extend(sub_categories)
    if 'categories' in parameters:
        categories = parameters["categories"].split(',')
        placeholders = ', '.join(['%s'] * len(categories))
        filters.append(f"category IN ({placeholders})")
        params.extend(categories)
    # search for one or many aircrafts that relate to document
    if 'aircrafts' in parameters:
        aircrafts = parameters["aircrafts"].split(',')
        placeholders = " OR ".join(["FIND_IN_SET(%s, aircrafts) > 0"] * len(aircrafts))
        filters.append(f"({placeholders})")
        params.extend(aircrafts)
    # start date and end date of create_at
    if 'create_at' in parameters:
        create_at = parameters["create_at"].split(',')
        filters.append("created_at BETWEEN %s AND %s")
        params.extend(create_at)
    # archived or not
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"archived = {parameters["archived"]}")
    
    # no filters for users/staff that relate documents
    # if they want to reference go to notices
    # or create many to many table again between documents and users/staff
    # but it's very complex to filter by users/staff and roles
    
    # if there is any filter add base query
    if filters:
        query += " WHERE " + " AND ".join(filters)
    # must have because GROUP_CONCAT
    query += " GROUP BY document_id "
    # if doesnt provide a sort column default is pk of documents
    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        # Add other valid column names if necessary
        valid_columns = ["document_id", "file_name", "email", "archived", "created_at", "sub_category", "category", "aircrafts"]
        if parameters["sort_column"] in valid_columns:
            # asc if true, desk if false
            order = 'ASC' if parameters["asc"] == 'true' else 'DESC'
            # in this part must parse as str cannot use binding because sort_column cannot be str
            query += f" ORDER BY {parameters["sort_column"]} {order}"
    
    # finish prepare query and params
    print(query)
    print(params)
    return query, params

def limit_query(parameters):
    nested_query = """
        SELECT 
        d.document_id, 
        d.file_name, 
        s.email AS author, 
        GROUP_CONCAT(r.role SEPARATOR ', ') AS roles,
        d.archived, 
        d.created_at, 
        sc.name AS subcategory, 
        c.name AS category,
        GROUP_CONCAT(a.name SEPARATOR ', ') AS aircrafts
        FROM documents AS d
        JOIN staff AS s 
        ON d.author_id = s.staff_id
        JOIN staff_roles AS sr
        ON s.staff_id = sr.staff_id
        JOIN roles AS r
        ON r.role_id = sr.role_id
        JOIN subcategories AS sc 
        ON sc.subcategory_id = d.subcategory_id
        JOIN categories AS c 
        ON sc.category_id = c.category_id
        LEFT OUTER JOIN aircraft_documents AS ad 
        ON ad.document_id = d.document_id
        LEFT OUTER JOIN aircrafts AS a 
        ON ad.aircraft_id = a.aircraft_id
        WHERE d.deleted_at IS Null
        
    """
    # Define limit if any
    limits = []
    params = []
    # Author limit
    if 'limit_author' in parameters:
        limits.append("s.email = %s")
        params.append(parameters["limit_author"])
    if 'limit_roles' in parameters:
        roles = parameters["limit_roles"].split(',')
        placeholders = ', '.join(['%s'] * len(roles))
        limits.append(f"r.role IN ({placeholders})")
        params.extend(roles)
    # Aircrafts limit
    if 'limit_aircrafts' in parameters:
        aircrafts = parameters["limit_aircrafts"].split(',')
        placeholders = ', '.join(['%s'] * len(aircrafts))
        limits.append(f"a.name IN ({placeholders})")
        params.extend(aircrafts)
    # Sub-categories limit
    if 'limit_subcategories' in parameters:
        sub_categories = parameters["limit_subcategories"].split(',')
        placeholders = ', '.join(['%s'] * len(sub_categories))
        limits.append(f"sc.name IN ({placeholders})")
        params.extend(sub_categories)
    # Categories limit  
    if 'limit_categories' in parameters:
        sub_categories = parameters["limit_categories"].split(',')
        placeholders = ', '.join(['%s'] * len(sub_categories))
        limits.append(f"c.name IN ({placeholders})")
        params.extend(sub_categories)

    if limits:
        nested_query += " AND ( " + " OR ".join(limits) + " ) "
    nested_query += " GROUP BY d.document_id "
    return nested_query, params

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