import os
import json
import timeit
import mysql.connector
from mysql.connector import Error
from mysql.connector.abstracts import MySQLCursorAbstract
from functools import wraps
from datetime import datetime
from typing import Any

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

# check body is JSON
def parse_body(body: Any) -> dict:
    print(body)
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            # Log the error for debugging
            print(f"Error decoding JSON: {e}")
            return {}
    elif isinstance(body, dict):
        return body
    else:
        raise ValueError("Body is not JSON")

# connect to db
def connect_to_db():
    return mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database="adsats_database"
    )

# return JSON response
def json_response(status_code: int, body: Any) -> dict:
    response = {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_headers
        },
        'body': json.dumps(body, indent=4, separators=(',', ':'), cls=DateTimeEncoder)
    }
    print(response)
    return response

# for dump datetime json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# timing how long function take
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Start {func.__name__}")
        _start_time = timeit.default_timer()
        _result = func(*args, **kwargs)
        _end_time = timeit.default_timer()
        print(f"{func.__name__} took {_end_time - _start_time} seconds")
        return _result
    return wrapper