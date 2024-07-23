from get_method import get_method
from helper import json_response, timer


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
    else:
        # Return method not allowed response for unsupported methods
        return json_response(405, "Method not allowed")


################################################################################