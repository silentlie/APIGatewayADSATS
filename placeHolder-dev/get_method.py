from mysql.connector import Error
import mysql.connector
import os

def get_method(body):
    try:
        query = read_file("adsats_database.sql")
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "adsats_database",
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, multi= True)
        if query.strip().upper().startswith("SELECT"):
            
            results = cursor.fetchall()
            print(results)
            for row in results:
                print(row)
        else:
            connection.commit()
            print("Query executed successfully and changes committed")
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
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
        'body': "Succeed"
    }
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
