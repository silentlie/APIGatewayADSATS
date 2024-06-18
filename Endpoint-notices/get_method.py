from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def get_method(parameters):

    ## Get all notices - for table view
    
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
            'headers': headers(),
            'body': json.dumps(response, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
        }
  
    except Error as e:
        print(f"Error: {e._full_msg}")
        
        return {
            'statusCode': 500,
            'headers': headers(),
            'body': json.dumps(e._full_msg)
        }
        
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def build_query(parameters):
    
    query = """
    SELECT 
        n.notice_id,
        s.email AS author,
        GROUP_CONCAT(DISTINCT r.role SEPARATOR ', ') AS roles,
        n.category,
        n.subject,
        n.resolved,
        n.issued,
        n.archived,
        n.notice_at,
        n.deadline_at
    FROM notices AS n
   	JOIN staff AS s 
    ON s.staff_id = n.author_id
    JOIN staff_roles AS sr
    ON s.staff_id = sr.staff_id
    JOIN roles AS r
    ON r.role_id = sr.role_id
    """
    
    filters = []
    params = []

    if 'staff_id' in parameters:
        query += " JOIN notifications AS nf ON nf.notice_id = n.notice_id "
        filters.append(" nf.staff_id = %s")
        params.append(parameters["staff_id"])

    # only return notices that this user is received
    query += " WHERE n.deleted_at is Null"
        
    if 'search' in parameters:
        filters.append("subject LIKE %s")
        params.append(parameters["search"])
    
    if 'categories' in parameters:
        categories = parameters["category"].split(',')
        placeholders = ', '.join(['%s'] * len(categories))
        filters.append(f"category IN ({placeholders})")
        params.extend(categories)
    
    if 'roles' in parameters:
        roles = parameters["roles"].split(',')
        placeholders = ', '.join(['%s'] * len(roles))
        filters.append(f"r.role IN ({placeholders})")
        params.extend(roles)
    
    if 'authors' in parameters:
        emails = parameters["authors"].split(',')
        placeholders = ', '.join(['%s'] * len(emails))
        filters.append(f"s.email IN ({placeholders})")
        params.extend(emails)
        
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"n.archived = {parameters["archived"]}")

    if 'resolved' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["resolved"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"resolved = {parameters["resolved"]}")
        
    if 'notice_at' in parameters:
        notice_at = parameters["notice_at"].split(',')
        filters.append("notice_at BETWEEN %s AND %s")
        params.extend(notice_at)

    if 'deadline_at' in parameters:
        deadline_at = parameters["deadline_at"].split(',')
        filters.append("n.deadline_at BETWEEN %s AND %s")
        params.extend(deadline_at)
    # if there is any filter add base query
    if filters:
        query += " AND " + " AND ".join(filters)
    
    query += " GROUP BY n.notice_id"

    if 'sort_column' in parameters:
        # Ensure sort_column is a valid column name to prevent SQL injection
        # Add other valid column names if necessary
        valid_columns = ["notice_id", "email", "category", "subject", "resolved", "archived", "notice_at", "deadline_at"]
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

## HELPERS ##
# Response headers
def headers():
    return {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        }

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
