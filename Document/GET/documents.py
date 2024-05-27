import mysql.connector

# Endpoint: document/
def document(body):
    connection = None
    cur = None
      
    try:
        connection = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
            database="new_adsats_database"
        )
        
        print("Database connected correctly")
              
        user = body["user"]
        category_name = body.get("category_name")   
        aircraft_name = body.get("aircraft_name") 
        limit = body["limit"]
        page = body["page"]
        archived = body["archived"]
        
        offset = (page - 1) * limit
        
        print("Processing request for user", user)

        cur = connection.cursor()
        
        results = []

        if category_name and not aircraft_name:
            sql_statement_1 = """ 
                SELECT name, 
                        DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, 
                        archived
                FROM (
                    SELECT
                        d.file_name AS name, 
                        d.created_at AS created_at, 
                        d.archived AS archived
                    FROM categories AS c
                    INNER JOIN subcategories AS s 
                        ON c.category_id = s.category_id 
                    INNER JOIN documents AS d
                        ON d.subcategory_id = s.subcategory_id
                    WHERE c.name = %s
                ) AS subquery_alias
                WHERE archived = %s
                ORDER BY created_at DESC
                LIMIT %s
                OFFSET %s;
            """
            cur.execute(sql_statement_1, (category_name, archived, limit, offset))
            results = cur.fetchall()
            
        elif category_name and aircraft_name:
            sql_statement_2 = """
                SELECT name,
                       DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, 
                       archived
                FROM (
                    SELECT 
                        d.file_name AS name,
                        d.created_at AS created_at,
                        d.archived AS archived
                    FROM categories c
                    INNER JOIN subcategories AS s 
                        ON c.category_id = s.category_id
                    INNER JOIN documents AS d 
                        ON d.subcategory_id = s.subcategory_id
                    INNER JOIN aircraft_documents AS ad
                        ON ad.documents_id = d.document_id
                    INNER JOIN aircrafts a
                        ON a.aircraft_id = ad.aircrafts_id
                    WHERE c.name = %s AND a.name = %s
                ) AS subquery_alias
                WHERE archived = %s
                ORDER BY created_at DESC
                LIMIT %s
                OFFSET %s;
            """                         
            cur.execute(sql_statement_2, (category_name, aircraft_name, archived, limit, offset))
            results = cur.fetchall()
        
        elif aircraft_name and not category_name:
            sql_statement_3 = """
                SELECT name, 
                        DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, 
                        archived
                FROM (
                    SELECT 
                        d.file_name AS name,
                        d.created_at AS created_at,
                        d.archived AS archived 
                    FROM aircrafts AS a
                    INNER JOIN aircraft_documents AS ad 
                        ON a.aircraft_id = ad.aircrafts_id
                    INNER JOIN documents AS d 
                        ON d.document_id = ad.documents_id
                    WHERE a.name = %s
                ) AS subquery_alias
                WHERE archived = %s
                ORDER BY created_at DESC
                LIMIT %s
                OFFSET %s;
            """                       
            cur.execute(sql_statement_3, (aircraft_name, archived, limit, offset))
            results = cur.fetchall()
        elif not aircraft_name and not category_name:
            sql_statement_4 = """SELECT
                                file_name, DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, 
                                archived
                                FROM documents
                                WHERE archived = %s
                                LIMIT %s
                                OFFSET %s   
                                        """
            cur.execute(sql_statement_4, (archived, limit, offset))
            results = cur.fetchall()
                                        
        else:
            print("Insufficient parameters provided.")
            return None
        
        if results:
            for doc in results:
                print(doc)
            return results
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

response = document({
    "user": "user",
    #"category_name": "Audit",
     "aircraft_name": "AB-CDE",
    "limit": 10,
    "page": 1,
    "archived": 1
})
print('Response:', response)
