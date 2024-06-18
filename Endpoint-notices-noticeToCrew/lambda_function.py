import json
from post_method import post_method
from get_method import get_method

allowed_headers = 'OPTIONS,GET,POST'

def lambda_handler(event, context):
    method = event.get("httpMethod")
    bodyStr = event.get("body")
    parameters = event.get("queryStringParameters")
    
    print(f"Method: {method}")
    print(f"Body: {bodyStr}")
    print(f"Parameters: {parameters}")
    
    body = {}
    if isinstance(bodyStr, str):
        body = json.loads(bodyStr)
    else:
        body = bodyStr
    
    if method == "GET":
        return get_method(parameters)
    if method == "POST":
        return post_method(body)
    else:
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allowed_headers
            },
            'body': json.dumps("Method not allowed")
        }