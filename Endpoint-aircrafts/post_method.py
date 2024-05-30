from mysql.connector import Error
import datetime
import mysql.connector
import os

def post_method(body):
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database="adsats_database",
        )
        cursor = connection.cursor()
       

        # email = body.get("email", None)
        name = body.get("aircraft_name", None)
        status = body.get("status", None)
        start_at = body.get("start_at", None)
        emails = body.get("emails", None).split(",")


        if start_at:
            start_at = datetime.datetime.now()
     
        query2 = """
            INSERT INTO aircrafts (name,status,start_at)
            Values (%s,%s,%s)  
        """
        cursor.execute(query2, (name, status, start_at))
        connection.commit()  # Commit changes
       
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
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
        'body': "Succeed"
    }
