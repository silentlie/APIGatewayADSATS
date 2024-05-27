import mysql.connector

# Endpoint: document/
def document(body):
    connection = None
    cur = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
            database="new_adsats_database"
        )

        print("Database connected correctly")

        user = body["user"]
        category_name = body.get("category_name")
        aircraft_name = body.get("aircraft_name")
        limit = body["limit"]
        page = body["page"]
        archived = body["archived"]

        offset = (page - 1) * limit

        print("Processing request for user", user)

        cur = connection.cursor()

        # Call the stored procedure
        cur.callproc('GetDocuments', [category_name, aircraft_name, limit, offset, archived])

        # Fetch the results from the procedure
        results = []
        for result in cur.stored_results():
            results = result.fetchall()

        if results:
            for doc in results:
                print(doc)
            return results
        else:
            print(None)
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

response = document({
    "user": "user",
    # "category_name": "Audit",
    "aircraft_name": "AB-CDE",
    "limit": 10,
    "page": 1,
    "archived": 1
})
print('Response:', response)
import mysql.connector

# Endpoint: document/
def document(body):
    connection = None
    cur = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
            database="new_adsats_database"
        )

        print("Database connected correctly")

        user = body["user"]
        category_name = body.get("category_name")
        aircraft_name = body.get("aircraft_name")
        limit = body["limit"]
        page = body["page"]
        archived = body["archived"]

        offset = (page - 1) * limit

        print("Processing request for user", user)

        cur = connection.cursor()

        # Call the stored procedure
        cur.callproc('GetDocuments', [category_name, aircraft_name, limit, offset, archived])

        # Fetch the results from the procedure
        results = []
        for result in cur.stored_results():
            results = result.fetchall()

        if results:
            for doc in results:
                print(doc)
            return results
        else:
            print(None)
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print('Database connection closed')

response = document({
    "user": "user",
    # "category_name": "Audit",
    "aircraft_name": "AB-CDE",
    "limit": 10,
    "page": 1,
    "archived": 1
})
print('Response:', response)
