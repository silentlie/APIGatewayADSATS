from post_method import post_method
from get_method import get_method
from patch_method import patch_method
from delete_method import delete_method
from helper import json_response, timer, parse_body, Any

@timer
def lambda_handler(
    event: dict, 
    context: dict
) -> dict:
    method = event.get("httpMethod")
    assert isinstance(method, str)
    print(method)
    if method == "OPTIONS":
        return json_response(200, "OK")
    elif method == "GET":
        parameters = event.get("queryStringParameters")
        assert isinstance(parameters, dict)
        print(parameters)
        return get_method(parameters)
    elif method == "POST":
        body = parse_body(event.get("body"))
        return post_method(body)
    elif method == "PATCH":
        body = parse_body(event.get("body"))
        return patch_method(body)
    elif method == "DELETE":
        body = parse_body(event.get("body"))
        return delete_method(body)
    else:
        return json_response(405, "Method not allow")
    
#===============================================================================