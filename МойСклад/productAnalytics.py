from constants import *
import mysqlConnection
import moyskladConnection

dbConnection, dbCursor = mysqlConnection.getConnection()
attributeArr = mysqlConnection.getEntityAttributes('product', dbCursor)
skladProduct = moyskladConnection.getProduct('E8403212--', attributeArr)
savedProduct = mysqlConnection.saveEntity('product', skladProduct, dbCursor, dbConnection, True)
print("saved product", savedProduct)
mysqlConnection.closeConnection(dbConnection, dbCursor)