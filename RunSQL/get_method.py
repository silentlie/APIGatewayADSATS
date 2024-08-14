from helper import Error, connect_to_db, json_response


def get_method(parameters):
    """ """
    connection = None
    cursor = None
    return_body = None
    status_code = 500
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        query = read_file(parameters["file_name"])
        # Determine if the query starts with SELECT
        is_select_query = query.strip().upper().startswith("SELECT")
        multi = not is_select_query

        # Execute query with the appropriate multi parameter
        if multi:
            for result in cursor.execute(query, multi=True): # type: ignore
                if result:
                    return_body = result.fetchall()
                    print(return_body)
        else:
            cursor.execute(query)
            return_body = cursor.fetchall()
            print(return_body)

        status_code = 200
    except Error as e:
        # Handle SQL error
        return_body = {"SQL_error": e._full_msg}
        if e.errno == 1062:
            status_code = 409  # Conflict error
    except Exception as e:
        # Handle general error
        return_body = {"error": str(e)}
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    response = json_response(status_code, return_body)
    print(response)
    return response


# Read file
def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

parameters = {"file_name": r"G:\ADSATS\APIGatewayADSATS\RunSQL\07.08.2024.sql"}
get_method(parameters)