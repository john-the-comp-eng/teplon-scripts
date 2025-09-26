import mysql.connector

class mySqlConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="secret",  # Replace with your MySQL password
                database="teplon"  # Replace with your database name
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database.")

            # Example: Execute a query
            self.cursor.execute("SELECT VERSION()")
            version = self.cursor.fetchone()
            print(f"MySQL Version: {version[0]}")

        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
            return None
        except Exception as e:
            print(f"Exception encountered: {e}")

    def closeConnection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")
        else:
            print("No connection found to close")

    def buildDictionaryFromData(self, attributes, data):
        newDict = {}
        for i in range(0, len(data)):
            newDict[attributes[i]] = data[i]
        return newDict

    def getEntityAttributes(self, entity):
        self.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'teplon' AND TABLE_NAME = '{entity}'")
        resultArr = self.cursor.fetchall()
        attributeArr = []
        for resultLine in resultArr:
            attributeArr.append(resultLine[0])
        return attributeArr

    def saveEntity(self, entity, attributeArr, dictionary, log=False):
        id = dictionary["id"]
        insertAttributes = ','.join(dictionary.keys())
        queryAttributes = ','.join(attributeArr)
        attributeValues = ','.join(list(map(lambda val: "'" + str(val) + "'", dictionary.values())))
        updateSql = self.updateEntity(entity, dictionary, False)
        query = f"""
                    INSERT INTO {entity} ({insertAttributes})
                    VALUES ({attributeValues}) ON DUPLICATE KEY UPDATE id = id;
                    {updateSql};
                    SELECT {queryAttributes} FROM {entity} WHERE id = '{id}';
                """
        
        if log:
            print(query)

        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            while cursor.nextset():
                result = cursor.fetchall()
                if len(result):
                    results.append(self.buildDictionaryFromData(attributeArr, result[0]))

        if len(results) != 1:
            raise Exception("Save entity query by id returned more than one result")
        else:
            return results[0]

    def updateEntity(self, entity, dictionary, execute=True, log=False):
        id = dictionary["id"]
        dictionary.pop("id")

        settingValues = ",".join(map(lambda attr: attr+"='"+str(dictionary[attr])+"'", dictionary))
        query = f"""
                    UPDATE {entity} SET {settingValues} WHERE id = '{id}'
                """
        if log:
            print(query)

        if execute:
            self.cursor.execute(query)
        else:
            return query