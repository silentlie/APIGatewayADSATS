import json
def post_method(body):
    # connect to database
    # retrieve the data/json file in body
    # insert main category if need
    # insert sub category if need
    # retrieve user_id
    # insert document
    # insert aircraft document if need
    # 
    
    
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        'body': body
    }