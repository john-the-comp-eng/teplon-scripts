import mysql.connector

class mySqlConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="35.228.178.34",
                user="root",  # Replace with your MySQL username
                password="2>\jjC[pV:ir<{O2",  # Replace with your MySQL password
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
        attributes = []
        for resultLine in resultArr:
            attributes.append(resultLine[0])
        return attributes

    def saveEntity(self, entity, attributes, dictionary, execute=True, log=False):
        for key in list(dictionary.keys()):
            if not dictionary[key]:
                dictionary.pop(key)
        
        id = dictionary["id"]
        insertAttributes = ','.join(dictionary.keys())
        queryAttributes = ','.join(attributes)
        attributeValues = ','.join(list(map(lambda val: "'" + str(val) + "'", dictionary.values())))
        updateSql = self.updateEntity(entity, dictionary, False)
        query = f"""
                    INSERT INTO {entity} ({insertAttributes})
                    VALUES ({attributeValues}) ON DUPLICATE KEY UPDATE id = id;
                    {updateSql};
                    SELECT {queryAttributes} FROM {entity} WHERE id = '{id}';
                """
        if not execute:
            return query

        if log:
            print(query)

        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            while cursor.nextset():
                result = cursor.fetchall()
                if len(result):
                    results.append(self.buildDictionaryFromData(attributes, result[0]))

        if log:
            print(results)
        if len(results) != 1:
            raise Exception("Save entity query by id returned more than one result")
        else:
            return results[0]
        
    def saveEntities(self, entity, attributes, dicitonaries, log=False):
        query = ""
        for dictionary in dicitonaries:
            query += self.saveEntity(entity, attributes, dictionary, False, False)
        
        if log:
            print(query)
        
        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            while cursor.nextset():
                result = cursor.fetchall()
                if len(result):
                    results.append(self.buildDictionaryFromData(attributes, result[0]))
        if log:
            print(results)

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
        
    def getEntries(self, entity, attributes, condition="TRUE", log=False):
        queryAttributes = ','.join(attributes)
        query = f"""
                    SELECT {queryAttributes} FROM {entity} WHERE {condition};
                """
        if log:
            print(query)

        entries = []
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for result in results:
            entries.append(self.buildDictionaryFromData(attributes, result))
        
        if log:
            print(results)

        return entries
        
