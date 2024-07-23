from delete_method import delete_method
from get_method import get_method
from helper import json_response, parse_body, timer
from patch_method import patch_method
from post_method import post_method


@timer
def lambda_handler(event: dict, context: dict) -> dict:
    """
    AWS Lambda handler function to process incoming API requests.

    Args:
        event (dict): The event dict containing the request data.
        context (dict): The context dict providing runtime information to the handler.

    Returns:
        dict: The HTTP response dictionary with status code, headers, and body.
    """
    # Extract the HTTP method from the event
    method = event.get("httpMethod")
    assert isinstance(method, str), "httpMethod must be a string"
    print(f"Received request with method: {method}")

    # Handle different HTTP methods
    if method == "OPTIONS":
        # Return OK response for preflight requests
        return json_response(200, "OK")
    elif method == "GET":
        # Handle GET request with query parameters
        parameters = event.get("queryStringParameters")
        assert isinstance(
            parameters, dict
        ), "queryStringParameters must be a dictionary"
        # print(f"Query parameters: {parameters}")
        return get_method(parameters)
    elif method == "POST":
        # Handle POST request with body parsing
        body = parse_body(event.get("body"))
        return post_method(body)
    elif method == "PATCH":
        # Handle PATCH request with body parsing
        body = parse_body(event.get("body"))
        return patch_method(body)
    elif method == "DELETE":
        # Handle DELETE request with body parsing
        body = parse_body(event.get("body"))
        return delete_method(body)
    else:
        # Return method not allowed response for unsupported methods
        return json_response(405, "Method not allowed")


################################################################################
