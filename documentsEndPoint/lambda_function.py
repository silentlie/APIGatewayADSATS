import json
from post_method import post_method
from get_method import get_method
from put_method import put_method
from patch_method import patch_method
from delete_method import delete_method
def lambda_handler(event, context):
    method = event.get("httpMethod")
    body = event.get("body")
    parameters = event.get("queryStringParameters")
    print(method)
    print(body)
    print(parameters)
    if method == "GET":
        return get_method(parameters)
    if method == "PUT":
        return put_method(body)
    if method == "POST":
        return post_method(body)
    if method == "PATCH":
        return patch_method(body)
    if method == "DELETE":
        return delete_method(body)
    else:
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH,DELETE'
            },
            'body': json.dumps("Method now allow")
        }