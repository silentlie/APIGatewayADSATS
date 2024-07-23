import decimal
import json
import os
from datetime import datetime

import mysql.connector
from mysql.connector import Error

allowed_headers = "OPTIONS,POST,GET,PATCH"


def get_method(parameters):
    try:
        connection = connect_to_db()
        query, params = build_query(parameters)
        cursor = connection.cursor(dictionary=True)

        query += " LIMIT %s OFFSET %s"
        limit = int(parameters["limit"])
        offset = int(parameters["offset"])
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Original: SUM(CASE WHEN n.deadline_at < NOW() THEN 1 ELSE 0 END) AS overdue
        # Modified by Carole 16/06 to have overdue items being those that are past due date and unread
        unread_query = """
        SELECT
            SUM(CASE WHEN nf.status = 0 THEN 1 ELSE 0 END) AS unread,
            SUM(CASE WHEN nf.status = 0 AND n.deadline_at < NOW() THEN 1 ELSE 0 END) AS overdue
        FROM notifications AS nf
        JOIN notices AS n
        ON nf.notice_id = n.notice_id
        WHERE (nf.status = 0 OR n.deadline_at < NOW())
        AND nf.staff_id = %s
        AND n.archived = false
        AND n.deleted_at IS Null
        """
        cursor.execute(unread_query, [int(parameters["staff_id"])])
        count = cursor.fetchone()

        response = {
            "rows": rows,
            # Convert Decimal to float if necessary
            "count": {
                k: float(v) if isinstance(v, decimal.Decimal) else v
                for k, v in count.items()
            },  # type: ignore
        }

        return {
            "statusCode": 200,
            "headers": headers(),
            "body": json.dumps(
                response, indent=4, separators=(",", ":"), cls=DateTimeEncoder
            ),
        }

    except Error as e:
        print(f"Error: {e._full_msg}")

        return {
            "statusCode": 500,
            "headers": headers(),
            "body": json.dumps(e._full_msg),
        }

    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def build_query(parameters):
    query = """
        SELECT
        	n.notice_id,
            n.subject,
            s.email,
            nf.status AS status,
            nf.read_at
        FROM notices AS n
       	JOIN notifications AS nf
        ON nf.notice_id = n.notice_id
        JOIN staff AS s
        ON s.staff_id = n.author_id
    """
    query += " WHERE nf.staff_id = %s "
    query += " AND n.deleted_at IS Null"
    query += " AND n.archived = false"
    query += " ORDER BY nf.status"
    params = [int(parameters["staff_id"])]

    return query, params


## HELPERS ##
# Response headers
def headers():
    return {
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": allowed_headers,
    }


def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get("HOST"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        database="adsats_database",
    )


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)  # Convert Decimal to float
        return super().default(obj)
