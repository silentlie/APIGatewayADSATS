from mysql.connector import Error
import mysql.connector
import os

def get_method(parameters):
    try:
        
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "",
        )
        cursor = connection.cursor()
        query = "SELECT "
        name = parameters.get('name')



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
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        'body': "Succeed"
    }
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()