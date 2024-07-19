import json
from get_method import get_method

allowed_headers = 'OPTIONS,POST,GET,PATCH,DELETE'

def lambda_handler(event, context):
    method = event.get("httpMethod")
    body_str = event.get("body")
    parameters = event.get("queryStringParameters")

    print(method)
    print(body_str)
    print(parameters)
    
    if method == "OPTIONS":
        return {
            'statusCode': 200,
            'headers': headers(),
            'body': json.dumps("OK")
        }
    elif method == "GET":
        return get_method()
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
## HELPERS ##