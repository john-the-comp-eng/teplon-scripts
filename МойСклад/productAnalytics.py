from constants import *
from mysqlConnection import mySqlConnection
from MoySkladEntities.product import Product

def saveProduct(article):
    attributeArr = dbObj.getEntityAttributes('product')
    skladProduct = productObj.get(article, attributeArr)
    savedProduct = dbObj.saveEntity('product', attributeArr, skladProduct)
    saveFilters = False
    if not savedProduct["demandFilterUrl"]:
        filterUrl = productObj.getFilterUrl(article, "demand")
        if filterUrl:
            savedProduct["demandFilterUrl"] = productObj.getFilterUrl(article, "demand")
            saveFilters = True
    if not savedProduct["supplyFilterUrl"]:
        filterUrl = productObj.getFilterUrl(article, "supply")
        if filterUrl:
            savedProduct["supplyFilterUrl"] = productObj.getFilterUrl(article, "supply")
            saveFilters = True
    if saveFilters:
        savedProduct = dbObj.saveEntity('product', attributeArr, savedProduct)

dbObj = mySqlConnection()
productObj = Product()
# article = 'E8403212--'
article = '065150'
product = saveProduct(article)

dbObj.closeConnection()
