import mysql.connector


def document(body):
    connection = None
    cur = None
      
    try:
        connection = mysql.connector.connect(
            host ="localhost",
            username = "root",
            password ="",
            database="adsats_database"
        )
        
        print("Database connected correctly")
              
    # Endpoint:documents/
    
        user = body["user"]
        category_name = body.get("category_name")   
        aircraft_name = body.get("aircraft_name")
        
        print("procceesing request for user",user)

    #create a cursor
    
        cur = connection.cursor()
        
        # when select
        # just a category name
        if (category_name and not aircraft_name):
            sql_statement_1 = """   SELECT d.name
                                    FROM categories As c
                                    INNER JOIN subcategories s ON  c.id = s.categories_id 
                                    INNER JOIN documents AS d ON  d.subcategory_id = s.subcategory_id
                                    WHERE  c.name =%s """
            
            cur.execute(sql_statement_1,(category_name,))
            category_result = cur.fetchall()
            print(len(category_result))
            
            if category_result:
            
                for doc in category_result:
                    print (doc)
                    
            else:
                print(None)   
                
        # when select aircraft and category        
        elif (category_name and aircraft_name):
            sql_statement_2 = """  SELECT 
                                        c.name AS category_name, 
                                        d.created_at AS document_date,
                                        a.name AS aircraft_name
                                    FROM categories c
                                    INNER JOIN subcategories s ON c.id = s.categories_id
                                    INNER JOIN documents d ON d.id = s.subcategory_id
                                    INNER JOIN aircrafts_links al ON al.documents_id = d.id
                                    INNER JOIN aircrafts a
                                    ON a.id = al.aircrafts_id
                                    WHERE c.name =%s AND a.name = %s""" 
                                     
            cur.execute(sql_statement_2,(category_name,aircraft_name))
            full_result = cur.fetchall()
            print(len(full_result))
        
            
            if full_result:
            
                for doc in full_result:
                    print (doc)
                    
            else:
                print(None) 
        
        #WHEN SELECT AIRCRAFTS
        elif (aircraft_name and not category_name):  
            sql_statement_3 = """SELECT a.id 
                                FROM aircrafts AS a
                                INNER JOIN aircrafts_links AS al ON a.id = al.aircrafts_id
                                INNER JOIN documents AS d ON d.id = al.documents_id
                                WHERE a.name = %s""" 
                                
            cur.execute(sql_statement_3,(aircraft_name,))
            aircraft_result = cur.fetchall()
            print(len(aircraft_result))
        
            
            if aircraft_result:
            
                for doc in aircraft_result:
                    print (doc)
                    
            else:
                print(None)    
                                
        else:
            print("Insufficient parameters provided.")
         
    except mysql.connector.Error as err:
        print (f"Error : {err}")
        return None
    
    finally: 
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected:
            connection.close()
            print('Database connection closed')
            
response = document({
    "user": "user",
   # "category_name" : "cat1",
    "aircraft_name" : "air1"
   
})
print('Response:',response)
