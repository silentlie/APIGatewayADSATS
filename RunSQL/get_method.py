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
        cursor.execute(query, multi=True)
        if query.strip().upper().startswith("SELECT"):
            return_body = cursor.fetchall()
            print(return_body)
            for row in return_body:
                print(row)
        else:
            connection.commit()
            return_body = "Query executed successfully and changes committed"
            print(return_body)

        status_code = 200
    except Error as e:
        # Handle SQL error
        return_body = {"error": e._full_msg}
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
