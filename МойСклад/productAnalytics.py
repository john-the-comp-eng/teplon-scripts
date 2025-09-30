from constants import *
from mysqlConnection import mySqlConnection
from MoySkladEntities.product import Product
from MoySkladEntities.event import Event

def saveProduct(dbObj: mySqlConnection, article):
    productController = Product()
    attributeArr = dbObj.getEntityAttributes('product')
    skladProduct = productController.get(article, attributeArr)
    savedProduct = dbObj.saveEntity('product', attributeArr, skladProduct)
    saveFilters = False
    if not savedProduct["demandFilterUrl"]:
        filterUrl = productController.getFilterUrl(article, "demand")
        if filterUrl:
            savedProduct["demandFilterUrl"] = productController.getFilterUrl(article, "demand")
            saveFilters = True
    if not savedProduct["supplyFilterUrl"]:
        filterUrl = productController.getFilterUrl(article, "supply")
        if filterUrl:
            savedProduct["supplyFilterUrl"] = productController.getFilterUrl(article, "supply")
            saveFilters = True
    if saveFilters:
        savedProduct = dbObj.saveEntity('product', attributeArr, savedProduct)
    return savedProduct

def saveEvents(dbObj: mySqlConnection, product):
    eventController = Event("demand", product)
    attributes = dbObj.getEntityAttributes('event')
    skladEvents = eventController.get(attributes)
    eventController = Event("supply", product)
    attributes = dbObj.getEntityAttributes('event')
    skladEvents = skladEvents + eventController.get(attributes)

dbObj = mySqlConnection()
# article = 'E8403212--'
article = '065150'
product = saveProduct(dbObj, article)
events = saveEvents(dbObj, product)

dbObj.closeConnection()
