import mysql.connector

# Endpoint: mynotification/SendNotice
def SendNotice(body):
    connection = None
    cur = None
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="adsats_database"
        )
        
        user = body["user"]
        roles = body["role"]  # List of roles
        emails = body["emails"]  # List of emails
        aircraft_names = body["aircraftNames"]  # List of aircraft names
        
        cur = connection.cursor()
        
        # Create placeholders for roles, emails, and aircraft names
        roles_placeholder = ', '.join(['%s'] * len(roles))
        emails_placeholder = ', '.join(['%s'] * len(emails))
        aircraft_names_placeholder = ', '.join(['%s'] * len(aircraft_names))
        
        # email not list -> email =%s ,...
        sql_statement = f"""
        SELECT DISTINCT email, members_id
        FROM (
            SELECT 
                m.id AS members_id,
                r.id AS rolesID,
                m.email AS email,
                NULL AS aircraft
            FROM 
                roles AS r
            INNER JOIN 
                members_has_roles AS mhr ON r.id = mhr.roles_id
            INNER JOIN 
                members AS m ON m.id = mhr.members_id
            WHERE 
                r.role IN ({roles_placeholder})
            UNION
            SELECT 
                m.id AS members_id,
                r.id AS rolesID,
                m.email AS email,
                NULL AS aircraft
            FROM 
                roles AS r
            INNER JOIN 
                members_has_roles AS mhr ON r.id = mhr.roles_id
            INNER JOIN 
                members AS m ON m.id = mhr.members_id
            WHERE 
                m.email IN ({emails_placeholder})
            UNION 
            SELECT
                m.id AS members_id,
                NULL AS rolesID,
                m.email AS email,
                a.name AS aircraft      
            FROM 
                aircrafts AS a
            INNER JOIN 
                aircrafts_has_members AS ahm ON a.id = ahm.aircrafts_id
            INNER JOIN
                members AS m ON m.id = ahm.members_id
            WHERE 
                a.name IN ({aircraft_names_placeholder})
        ) AS combined_results
        GROUP BY email, members_id
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
    "role": ["role1", "role2"],
    "emails": ["Ayhan@yahoo.com", "Sahar@example.com"],
    "aircraftNames": ["air2", "air3"]
})
print('Response:', response)
