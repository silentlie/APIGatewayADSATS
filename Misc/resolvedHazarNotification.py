import mysql.connector

#Endpoint :mynotification/resolvehazardreport
def ResolveHazardNotice(body) :
    
    connection = None
    cur = None
    
    try:
        
        connection = mysql.connector.connect(
            host ="localhost",
            username ="root" ,
            password ="" ,
            database="adsats_database"
            )
        
        user = body["user"]
        email = body["email"]
        limit = body["limit"]
        page = body["page"]
        
        #define variable for offset
        offset = (page - 1) * limit
        #create a cursor
        cur = connection.cursor()
        
#/Select subj notification date aircraft and resovled from notices where category = hazard report ,all of members  Order by resovled(0,1) ascending a and create_at  desending
#Sort by (resolved ->0 at first),date created  - Limit =10 or more records and offset
#(notices has category field name: hazard ,saftely notice
# due date -> deadline, notificationDate ->created-at, type of notification ->category
#resoved -> 0 or 1 statuse in notification -> read/unread
        Sql_statement = """
                            SELECT n.subject,nf.status,n.deadline_at,n.created_at,
                            a.name,n.category,n.resolved
                            FROM notices AS n
                            INNER JOIN aircrafts_has_notices AS ahn 
                            ON n.id = ahn.notices_id
                            INNER JOIN aircrafts AS a
                            ON ahn.aircrafts_id = a.id
                            INNER JOIN notifications as nf
                            ON nf.notices_id = notices.id
                            INNER JOIN members as m
                            ON m.id = n.members_id
                            WHERE m.email = %s 
                            ORDER BY n.resolved DESC , n.created_at DESC
                            LIMIT = %s
                            OFFSET = %s 
                        """
        cur.execute(Sql_statement,(email,limit,offset,))
    except mysql.connector.Error as err:
        print (f"Error : {err}")
        return None
    
    finally: 
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected:
            connection.close()
            print('Database connection closed')
            
response = ResolveHazardNotice({
    "user": "user",
    "email":"Shima@yahoo.com",
    "limit" :10,
    "page":2
   
})
print('Response:',response)
