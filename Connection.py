import mysql.connector



# Connection to the database
connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "adsats_database"
    )
