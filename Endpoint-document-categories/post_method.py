from mysql.connector import Error
import mysql.connector
import os
def post_method(body):
    try:
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "adsats_database",
        )
        cursor = connection.cursor()
        name = body.get("name", default=None)
        emails = body.get("emails", default=None).split(',')
        timeRange = body.get("timeRange", default=None).split(',')
        archived = body.get("archived", default=None)
        aircrafts = body.get("aircrafts", default=None).split(',')
        columnName = body.get("clumnName", default=None)
        asc = body.get("asc", default=None)
        limit = body.get("limit")
        offset = body.get("offset")
        query = """
        SELECT d.document_id, d.file_name, u.email, d.archived, d.created_at, d.modified_at, ss.name, GROUP_CONCAT(a.name SEPARATOR ', ') 
        FROM documents AS d
        JOIN users AS u ON d.uploaded_by_id = u.user_id
        JOIN subcategories AS ss ON ss.subcategory_id = d.subcategory_id
        JOIN aircraft_documents AS ad ON ad.documents_id = d.document_id
        JOIN aircrafts AS a ON ad.aircrafts_id = a.aircraft_id
        """
        conditions = []
        params = []
        if name is not None:
            conditions.append("d.file_name = %s")
            params.append(name)
        if emails is not None:
            placeholders = ', '.join(['%s'] * len(emails))
            conditions.append(f"u.emails IN ({placeholders})")
            params.extend(emails)
        if timeRange is not None:
            conditions.append("d.created_at BETWEEN %s AND %s")
            params.extend(timeRange)
        if archived is not None:
            conditions.append("d.archived = %s")
            params.append(archived)
        if aircrafts is not None:
            placeholders = ', '.join(['%s'] * len(aircrafts))
            conditions.append(f"ad.aircraft_id IN ({placeholders})")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        if columnName is not None:
            query += "ORDER BY d.%s %s"
            params.append(columnName)
            if asc:
                params.append('ASC')
            else:
                params.append('DESC')
        query += "LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        for row in results:
            # need to convert to a list of dict/json
            print(row)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
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
        # this suppose to return all rows
        'body': "Succeed"
    }