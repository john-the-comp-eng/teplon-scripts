import mysql.connector

def getConnection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="secret",  # Replace with your MySQL password
            database="teplon"  # Replace with your database name
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("Connected to MySQL database.")

        # Example: Execute a query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version[0]}")
        return conn, cursor

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        return None
    except Exception as e:
        print(f"Exception encountered: {e}")

def closeConnection(conn, cursor):
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")
    else:
        print("No connection found to close")

def getEntityAttributes(entity, cursor):
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'teplon' AND TABLE_NAME = '{entity}'")
    resultArr = cursor.fetchall()
    attributeArr = []
    for resultLine in resultArr:
        attributeArr.append(resultLine[0])
    return attributeArr

def saveEntity(entity, dictionary, cursor, dbConnection, log=False):
    id = dictionary["id"]
    attributes = ','.join(dictionary.keys())
    attributeValues = ','.join(list(map(lambda val: "'" + str(val) + "'", dictionary.values())))
    query = (
                f"INSERT INTO {entity} ({attributes}) "
                f"VALUES ({attributeValues}) ON DUPLICATE KEY UPDATE id = id;"
                "" + updateEntity(entity, dictionary, cursor, dbConnection, False) + ";"
                f"SELECT * FROM {entity} WHERE id = '{id}';"
            )
    
    if log:
        print(query)
    cursor.execute(query)
    print("entity", entity)
    
def updateEntity(entity, dictionary, cursor, dbConnection, execute=True, log=False):
    id = dictionary["id"]
    dictionary.pop("id")
    query = (f"UPDATE {entity} SET " +
             f",".join(map(lambda attr: attr+"='"+str(dictionary[attr])+"'", dictionary)) + " " +
             f"WHERE id = '{id}'"
             )
    if log:
        print(query)

    if execute:
        cursor.execute(query)
    else:
        return query