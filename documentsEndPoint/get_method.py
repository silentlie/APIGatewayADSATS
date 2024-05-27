from datetime import datetime
import json
from mysql.connector import Error
import mysql.connector
import os
# I've refactor the code so it look a little different
def get_method(parameters):
    # error_message: this should have in every method
    error_message = ""
    try:
        # connect_to_db function is separate for easier to read
        connection = connect_to_db()
        cursor = connection.cursor()
        # build_query function is base on method for example this take parameters
        # the method return query and parameters for binding
        query, params = build_query(parameters)
        total_records = get_total_records(query, params, cursor)
        # for pagination must have in parameters of method
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
        results = cursor.fetchall()
        # create a response each row is array of data so response is array of array
        rows = []
        for row in results:
            rows.append(row)
            print(row)
        response = {
            "total_records": total_records,
            "rows": rows
        }
    # hanlding error
    except Error as e:
        print(f"Error: {e._full_msg}")
        error_message = e._full_msg
    finally:
        # close cursor and connection
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    # if error occur return 500 with error
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
    # if succeed return 200 with data
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
    SELECT d.document_id, d.file_name, u.email, d.archived, d.created_at, d.modified_at, s.name AS subcategory, c.name AS category
    , GROUP_CONCAT(a.name SEPARATOR ', ') AS aircrafts
    FROM documents AS d
    JOIN users AS u ON d.uploaded_by_id = u.user_id
    JOIN subcategories AS s ON s.subcategory_id = d.subcategory_id
    JOIN categories AS c ON s.category_id = c.category_id
    LEFT OUTER JOIN aircraft_documents AS ad ON ad.documents_id = d.document_id
    LEFT OUTER JOIN aircrafts AS a ON ad.aircrafts_id = a.aircraft_id
    """
    # define filters if any
    filters = []
    # parameters for binding
    params = []
    # name key in parameters of method should be "%aircraft%"
    if 'name' in parameters:
        filters.append("d.file_name LIKE %s")
        params.append(parameters["name"])
    # search for one or many emails/users/authors
    if 'emails' in parameters:
        emails = parameters["emails"].split(',')
        placeholders = ', '.join(['%s'] * len(emails))
        filters.append(f"u.email IN ({placeholders})")
        params.extend(emails)
    # start date and end date of create_at
    if 'timeRange' in parameters:
        time_range = parameters["timeRange"].split(',')
        filters.append("d.created_at BETWEEN %s AND %s")
        params.extend(time_range)
    # archived or not
    if 'archived' in parameters:
        filters.append("d.archived = %s")
        params.append(parameters["archived"])
    # search for one or many aircrafts that relate to document
    if 'aircrafts' in parameters:
        aircrafts = parameters["aircrafts"].split(',')
        placeholders = ', '.join(['%s'] * len(aircrafts))
        filters.append(f"ad.aircraft_id IN ({placeholders})")
        params.extend(aircrafts)
    # no filters for users that relate documents
    # if they want to reference go to notices
    # or create many to many table again between documents and users
    # but it's very complex to filter by users and roles
    
    # if there is any filter add base query
    if filters:
        query += " WHERE " + " AND ".join(filters)
    # must have because GROUP_CONCAT
    query += " GROUP BY d.document_id "
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

def get_total_records(query, params, cursor):
    total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    return result[0]

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)