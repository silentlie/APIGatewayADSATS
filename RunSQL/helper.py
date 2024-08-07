import json
import os
import timeit
from datetime import datetime
from functools import wraps
from typing import Any

import mysql.connector
from mysql.connector import Error  # noqa: F401
from mysql.connector.abstracts import MySQLCursorAbstract  # noqa: F401

# Allowed HTTP methods for CORS
allowed_headers = "OPTIONS,GET"


def parse_body(body: Any) -> dict:
    """
    Parses the body of a request to ensure it is JSON.

    Args:
        body (Any): The body of the request, which can be a JSON string or a dictionary.

    Returns:
        dict: The parsed JSON as a dictionary.

    Raises:
        ValueError: If the body is not a valid JSON string or dictionary.
    """
    print(body)
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            # Log the error for debugging
            # print(f"Error decoding JSON: {e}")
            return {}
    elif isinstance(body, dict):
        return body
    else:
        raise ValueError("Body is not JSON")


def connect_to_db():
    """
    Connects to the MySQL database using credentials from environment variables.

    Returns:
        mysql.connector.abstracts.MySQLConnectionAbstract: The connection object to the database.
    """
    return mysql.connector.connect(
        host=os.environ.get("HOST"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        database="adsats_database",
    )


def json_response(status_code: int, body: Any) -> dict:
    """
    Generates a JSON response with the given status code and body.

    Args:
        status_code (int): The HTTP status code for the response.
        body (Any): The body of the response, which will be JSON encoded.

    Returns:
        dict: The HTTP response dictionary with headers and body.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": allowed_headers,
        },
        "body": json.dumps(body, indent=4, separators=(",", ":"), cls=DateTimeEncoder),
    }


class DateTimeEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for datetime objects.

    Methods:
        default(self, o: Any): Encodes datetime objects to ISO format strings.
    """

    def default(self, o: Any):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def timer(func):
    """
    Decorator that prints the execution time of the decorated function.

    Args:
        func (Callable): The function to be timed.

    Returns:
        Callable: The wrapped function with timing.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Start {func.__name__}")
        _start_time = timeit.default_timer()
        _result = func(*args, **kwargs)
        _end_time = timeit.default_timer()
        print(f"{func.__name__} took {_end_time - _start_time} seconds")
        return _result

    return wrapper


################################################################################
