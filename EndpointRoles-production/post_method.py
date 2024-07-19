from helper import (
    connect_to_db,
    json_response,
    timer,
    Error,
    MySQLCursorAbstract
)

@timer
def post_method(
    body: dict
) -> dict:
    """
    Post method
    """
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        # Insert the new record and get the id
        role_id = insert_role(cursor, body)
        # Commits the transaction to make the insert operation permanent
        # If any error is raised, there'll be no commit
        connection.commit()
        return_body = role_id
        status_code = 200
    # Catch SQL exeption
    except Error as e:
        return_body = f"SQL Error: {e._full_msg}"
        # Error no 1062 means duplicate name
        if e.errno == 1062:
            # Code 409 means conflict in the state of the server
            status_code = 409
    # Catch other exeptions
    except Exception as e:
        return_body = f"SQL Error: {e}"
    # Close cursor and connection
    finally:
        if cursor:
            cursor.close()
            print("MySQL cursor is closed")
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    response = json_response(status_code, return_body)
    print (response)
    return response

@timer
def insert_role(
    cursor: MySQLCursorAbstract,
    body: dict
) -> int:
    """
    Insert new record and return id
    """
    query = """
    INSERT INTO roles (role_name, archived, created_at, description)
    VALUES (%s, %s, %s, %s)
    """
    params = [body["role_name"], body["archived"], body["created_at"], body["description"]]
    cursor.execute(query, params)
    cursor.execute("SELECT LAST_INSERT_ID()")
    role_id = cursor.fetchone()
    assert isinstance(role_id, int)
    print("Record inserted successfully with ID:", role_id)
    return role_id

#===============================================================================