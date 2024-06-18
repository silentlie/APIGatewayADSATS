import json
from mysql.connector import Error
import mysql.connector
import os
from datetime import datetime

allowed_headers = 'OPTIONS,POST,GET,PATCH'

def patch_method(body):
    try:
        connection = mysql.connector.connect(
            host= os.environ.get('HOST'),
            user= os.environ.get('USER'),
            password= os.environ.get('PASSWORD'),
            database= "adsats_database",
        )
        cursor = connection.cursor(dictionary=True)
        staff_id = body.get("staff_id", default=None)
        notice_id = body.get("notice_id", default=None)
        status = body.get("status", default=None)
        read_at = datetime.now()
        query = """
            UPDATE staff
            SET status = %s,
                read_at = %s,
            WHERE staff_id = %s
            AND notice_id = %s
        """
        params = [status, read_at, notice_id, staff_id]
        cursor.execute(query, params)
        connection.commit()
        
        query = """
            SELECT
        	n.notice_id,
            n.category,
            FROM notices AS n
            WHERE notice_id = %s
        """
        cursor.execute(query, (notice_id))
        result = cursor.fetchone
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allowed_headers
            },
            'body': json.dumps(result)
        }
    except Error as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")