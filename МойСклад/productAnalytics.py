from constants import *
from mysqlConnection import mySqlConnection
from MoySkladEntities.product import Product

dbObj = mySqlConnection()
productObj = Product()
attributeArr = dbObj.getEntityAttributes('product')
skladProduct = productObj.get('E8403212--', attributeArr)
savedProduct = dbObj.saveEntity('product', attributeArr, skladProduct, True)
if not savedProduct["filterUrl"]:
    pass
dbObj.closeConnection()
