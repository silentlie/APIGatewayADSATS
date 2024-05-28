import json
import mysql.connector
from mysql.connector import Error
import os

def get_method(parameters):
    error_message = ""
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query, params = build_query(parameters)
        total_records = get_total_records(query, params, cursor)

        query += " LIMIT %s OFFSET %s"
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])

        cursor.execute(query, params)
        results = cursor.fetchall()

        rows = []
        for row in results:
            rows.append(row)
            print(row)
        response = {
            "total_records": total_records,
            "rows": rows
        }

    except Error as e:
        print(f"Error: {e}")
        error_message = str(e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
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
        'body': json.dumps(response, indent=4, separators=(',', ':'))
    }

def build_query(parameters):
    roles = parameters.get('roles', '').split(',')
    emails = parameters.get('emails', '').split(',')
    aircraft_names = parameters.get('aircraftNames', '').split(',')

    roles_placeholder = ', '.join(['%s'] * len(roles))
    emails_placeholder = ', '.join(['%s'] * len(emails))
    aircraft_names_placeholder = ', '.join(['%s'] * len(aircraft_names))

    query = f"""
    SELECT DISTINCT email, user_id
    FROM (
        SELECT 
            u.user_id AS user_id,
            r.role_id AS role_id,
            u.email AS email,
            NULL AS aircraft
        FROM roles AS r
        INNER JOIN user_roles AS ur ON r.role_id = ur.role_id
        INNER JOIN users AS u ON u.user_id = ur.user_id
        -- WHERE r.role IN ({roles_placeholder})
            
        UNION
        
        SELECT 
            u.user_id AS user_id,
            r.role_id AS role_id,
            u.email AS email,
            NULL AS aircraft
        FROM roles AS r
        INNER JOIN user_roles AS ur ON r.role_id = ur.role_id
        INNER JOIN users AS u ON u.user_id = ur.user_id
        -- WHERE u.email IN ({emails_placeholder})
            
        UNION
        
        SELECT
            u.user_id AS user_id,
            NULL AS role_id,
            u.email AS email,
            a.name AS aircraft      
        FROM aircrafts AS a
        INNER JOIN aircraft_crew AS ac ON a.aircraft_id = ac.aircraft_id    
        INNER JOIN users AS u ON u.user_id = ac.user_id
        -- WHERE a.name IN ({aircraft_names_placeholder})
    ) AS combined_results
    """

    filters = []
    params = []
    if 'user_id' in parameters:
        filters.append("u.user_id LIKE %s")
        params.append(parameters["user_id"])
        
    if 'email' in parameters:
        filters.append("u.email LIKE %s")
        params.append(parameters["email"])
        
    if 'emails' in parameters:
        emails = parameters["emails"].split(',')
        emails_placeholder = ','.join(['%s'] * len(emails))
        filters.append(f"u.email IN ({emails_placeholder})")
        params.extend(emails)
    
    if 'roles' in parameters:
        roles = parameters["roles"].split(',')
        roles_placeholder = ','.join(['%s'] * len(roles))
        filters.append(f"r.role IN ({roles_placeholder})")
        params.extend(roles)
    
    if 'aircraftNames' in parameters:
        aircraft_names = parameters["aircraftNames"].split(',')
        aircraft_names_placeholder = ','.join(['%s'] * len(aircraft_names))
        filters.append(f"a.name IN ({aircraft_names_placeholder})")
        params.extend(aircraft_names)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " GROUP BY email, user_id"

    if 'sort_column' in parameters:
        order = 'ASC' if parameters.get("asc", 'false') == 'true' else 'DESC'
        query += f" ORDER BY u.{parameters['sort_column']} {order}"

    return query, params

def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="new_adsats_database"
    )

def get_total_records(query, params, cursor):
    total_query = "SELECT COUNT(*) as total_records FROM (" + query + ") AS initial_query"
    cursor.execute(total_query, params)
    result = cursor.fetchone()
    return result[0]
