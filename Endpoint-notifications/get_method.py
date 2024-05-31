from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    error_message = ""
    cursor = None
    try:
        connection = connect_to_db()
        query, params = build_query(parameters)
        
        total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
        cursor = connection.cursor()
        print(total_query)
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
            n.subject,
            u.email,
            nf.status AS status,
            nf.read_at
        FROM notices AS n
       	JOIN notifications AS nf 
        ON nf.notice_id = n.notice_id
        JOIN users AS u
        ON u.staff_id = n.author_id
        JOIN users AS uu
        ON uu.staff_id = nf.staff_id
		WHERE uu.email = "ccockingd@ask.com"
    """
    query += " WHERE uu.email = %s "
    query += " AND n.delete_at IS Null"
    
    filters = []
    params = []    
    params = [parameters["email"]]
    
    if 'subject' in parameters:
        filters.append("subject LIKE %s")
        params.append(parameters["subject"])
    
    if 'categories' in parameters:
        categories = parameters["category"].split(',')
        placeholders = ', '.join(['%s'] * len(categories))
        filters.append(f"category IN ({placeholders})")
        params.extend(categories)
    
    if 'emails' in parameters:
        emails = parameters["emails"].split(',')
        placeholders = ', '.join(['%s'] * len(emails))
        filters.append(f"u.email IN ({placeholders})")
        params.extend(emails)
        
    if 'archived' in parameters:
        # Ensure archived is a valid value to prevent SQL injection
        # Add other valid value if necessar
        valid_value = ["true", "false"]
        if parameters["archived"] in valid_value:
            # in this part must parse as str cannot use binding because bool cannot be str
            filters.append(f"archived = {parameters["archived"]}")

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
