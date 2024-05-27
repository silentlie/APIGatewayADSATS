from mysql.connector import Error
import mysql.connector
import os

def patch_method(body):
    try:
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "",
        )
        cursor = connection.cursor()





        
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            connection.commit()
            print(f"Query executed successfully and changes committed: {query}")
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
        'body': "Succeed"
    }
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()