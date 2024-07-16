import json
from post_method import post_method
from get_method import get_method
from patch_method import patch_method
from delete_method import delete_method

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def lambda_handler(event, context):
    method = event.get("httpMethod")
    body_str = event.get("body")
    parameters = event.get("queryStringParameters")
    print(method)
    print(body_str)
    print(parameters)
    body = {}
    if isinstance(body_str, str):
        body = json.loads(body_str)
    else:
        body = body_str
    if method == "GET":
        return get_method(parameters)
    if method == "POST":
        return post_method(body)
    if method == "PATCH":
        return patch_method(body)
    if method == "DELETE":
        return delete_method(body)
    else:
        return {
            'statusCode': 405,
            'headers': headers(),
            'body': json.dumps("Method now allow")
        }
    
## HELPERS ##
# Response headers
def headers():
    return {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': allowed_headers
    }