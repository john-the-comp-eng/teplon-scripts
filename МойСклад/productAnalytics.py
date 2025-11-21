from constants import *
from mysqlConnection import mySqlConnection
from MoySkladEntities.product import Product
from MoySkladEntities.event import Event

def saveProduct(dbObj: mySqlConnection, article):
    productController = Product()
    attributeArr = dbObj.getEntityAttributes('product')
    skladProduct = productController.get(article, attributeArr)
    if skladProduct is None:
        return None
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
    if len(skladEvents):
        dbObj.saveEntities("event", attributes, skladEvents)
    id=product['id']
    return dbObj.getEntries("event", attributes, f"product='{id}' ORDER BY moment DESC")
    
def calculateHistoricStock(dbObj: mySqlConnection, product, events, log=False):
    attributes = dbObj.getEntityAttributes('event')
    stock = product["stock"]
    stockDelta = None
    for i in range(len(events)):
        if not stockDelta:
            stockDelta = 0
        else:
            stock += stockDelta
        events[i]['stock'] = stock if stock else '0'

        match events[i]['eventType']:
            case "demand":
                stockDelta = events[i]['quantity']
            case "supply":
                stockDelta = -events[i]['quantity']
            case _:
                raise Exception("invalid product event type provided for event " + events[i]['id'])
    dbObj.saveEntities("event", attributes, events)

dbObj = mySqlConnection()
productController = Product()

articles = productController.getArticlesByFilterName(VAILLANT_PARTS_FILTER_ID)

count = 1
for article in articles:
    product = saveProduct(dbObj, article)
    if product is None:
        print(f"Cannot process article {article}: {count}")
        count += 1
        continue
    events = []
    events = saveEvents(dbObj, product)
    if len(events):
        calculateHistoricStock(dbObj, product, events)
    print(f"Article {article} processed: {count}")
    count += 1

dbObj.closeConnection()
