import json

from get_method import get_method

def lambda_handler(event, context):
    method = event["httpMethod"]
    body = event["body"]
    
    print(method)
    print(body)
    if method == "GET":
        return get_method(body)
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,'
            },
            'body': json.dumps(event["httpMethod"])
        }
