import mysql.connector

# Endpoint:notice/SendNotice
def SendNotice(body):
    connection = None
    cur = None
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="new_adsats_database"
        )
        
        user = body["user"]
        # list of inputs
        roles = body["role"]  
        emails = body["emails"]  
        aircraft_names = body["aircraftNames"]  
        
        cur = connection.cursor()
        
        # Create placeholders for roles, emails, and aircraft names
        roles_placeholder = ', '.join(['%s'] * len(roles))
        emails_placeholder = ', '.join(['%s'] * len(emails))
        aircraft_names_placeholder = ', '.join(['%s'] * len(aircraft_names))
        
        sql_statement = f"""
        SELECT DISTINCT email, user_id
        FROM (
            SELECT 
                u.user_id AS user_id,
                r.role_id AS role_id,
                u.email AS email,
                NULL AS aircraft
                
            FROM 
                roles AS r
            INNER JOIN 
                user_roles AS ur 
            ON 
                r.role_id = ur.role_id
                
            INNER JOIN 
                users AS u 
            ON 
                u.user_id = ur.user_id
            WHERE 
                r.role IN ({roles_placeholder})
                
            UNION
            
            SELECT 
                u.user_id AS user_id,
                r.role_id AS role_id,
                u.email AS email,
                NULL AS aircraft
            FROM 
                roles AS r
            INNER JOIN 
                user_roles AS ur 
            ON 
                r.role_id = ur.role_id
            INNER JOIN 
                users AS u ON u.user_id = ur.user_id
            WHERE 
                u.email IN ({emails_placeholder})
                
            UNION
             
            SELECT
                u.user_id AS user_id,
                NULL AS role_id,
                u.email AS email,
                a.name AS aircraft      
            FROM 
                aircrafts AS a
            INNER JOIN 
                aircraft_crew AS ac
            ON 
                a.aircraft_id = ac.aircraft_id    
            INNER JOIN
                users AS u 
            ON 
                u.user_id = ac.user_id
            WHERE 
                a.name IN ({aircraft_names_placeholder})
        ) AS combined_results
        GROUP BY email, user_id
        """
        
        # Combine roles, emails, and aircraft names into parameters list
        params = roles + emails + aircraft_names
        
        cur.execute(sql_statement, params)
        result = cur.fetchall()
        
        if result:
            for record in result:
                print(record)
            return result
        else:
            print(None)
            return None
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

response = SendNotice({
    "user": "user",
    "role": ["administrator", "cabin attendants"],
    "emails": ["amckeran2@instagram.com", "adalgarnowchi@cnbc.com"],
    "aircraftNames": ["AB-CDE", "KP-SDA"]
})
print('Response:', response)
