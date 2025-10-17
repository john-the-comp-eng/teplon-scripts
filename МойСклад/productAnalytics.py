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
    if len(skladEvents):
        dbObj.saveEntities("event", attributes, skladEvents)
    id=product['id']
    return dbObj.getEntries("event", attributes, f"product='{id}' ORDER BY moment DESC")
    
def calculateHistoricStock(dbObj: mySqlConnection, product, events, log=False):
    attributes = dbObj.getEntityAttributes('event')
    productController = Product()
    stock = productController.getStock(product['article'], log)
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
# BAXI
BaxiArticles_Processed = [
# articles = [
    'E8403330--', 'E8403336--', 'E8403345--', 'E8403309--', 'E8403212--', 'E8403214--', 'E8403218--', 'E8403224--', 'E8403230--', 'E8403236--', 'E8403206--', 'E8403209--', 'E8403312--', 'E8403314--', 'E8403318--', 'E8403324--', 
    'A7720023', 'A7720024', 'A7720025', 'A7720026', 'A7720027', 'A7720028', 'A7810404', 'A7785873', 'A7810446', 'A7114602', 'A7114600', 'A7114601', 'A7689653', 'A7689652', 'A7689651', 'A7689649', 'A7722037', 'A7722038', 'A7722039', 'A7810405', 'A7720022',
    '7219692--', '7219693--', '7219553--', '7219554--', '7219555--', '7685036--', '7106815--', '7104050--', '7104051--', '7104052--', '7221295', '7219688--', '7219689--', '7219690--', '7219691--', '7814105', '7814108', '7814104', '7813724', '7869249', '7869251', '7869250', '7869252', '7221296', '7671757--', '7612420', '7612419', '7612418', '7612421', '7659668--', '7659666--', '7659669--', '7659762--', '7659670--', '7860077', 
    'CSE46114354-', 'CSE46514354-', 'CSE46124354-', 'CSE46524354-', 'CSE46224354-', 'CSE46624354-', 'CSE45624366-', 'CSE45224366-', 'CSE45628366-', 'CSE45631366-', 'CSE45624358-', 'CSE45224358-', 'CSE45631358-', 'CSB45724358-', 'CSB45424358-', 'CSB45728358-', 'CSB45428358-', 'CSB45732358-',
    '100021538', '100022963', '100023035', '100021539', '100021540', '100021428', '100022347',
    'WHS43110060-', 'WHS43112060-', 'WHS43115060-', 'WHS43104560-', 'WHS43106560-', 'WHS43108560-', 
]
# articles = [
    # 'E8403330--', 'E8403336--', 'E8403345--', 'E8403309--', 'E8403212--', 'E8403214--', 'E8403218--', 'E8403224--', 'E8403230--', 'E8403236--', 'E8403206--', 'E8403209--', 'E8403312--', 'E8403314--', 'E8403318--', 'E8403324--', 
    # 'A7720023', 'A7720024', 'A7720025', 'A7720026', 'A7720027', 'A7720028', 'A7810404', 'A7785873', 'A7810446', 'A7114602', 'A7114600', 'A7114601', 'A7689653', 'A7689652', 'A7689651', 'A7689649', 'A7722037', 'A7722038', 'A7722039', 'A7810405', 'A7720022',
    # '7219692--', '7219693--', '7219553--', '7219554--', '7219555--', '7685036--', '7106815--', '7104050--', '7104051--', '7104052--', '7221295', '7219688--', '7219689--', '7219690--', '7219691--', '7814105', '7814108', '7814104', '7813724', '7869249', '7869251', '7869250', '7869252', '7221296', '7671757--', '7612420', '7612419', '7612418', '7612421', '7659668--', '7659666--', '7659669--', '7659762--', '7659670--', '7860077', 
    # 'CSE46114354-', 'CSE46514354-', 'CSE46124354-', 'CSE46524354-', 'CSE46224354-', 'CSE46624354-', 'CSE45624366-', 'CSE45224366-', 'CSE45628366-', 'CSE45631366-', 'CSE45624358-', 'CSE45224358-', 'CSE45631358-', 'CSB45724358-', 'CSB45424358-', 'CSB45728358-', 'CSB45428358-', 'CSB45732358-',
#     '100021538', '100022963', '100023035', '100021539', '100021540', '100021428', '100022347',
#     'WHS43110060-', 'WHS43112060-', 'WHS43115060-', 'WHS43104560-', 'WHS43106560-', 'WHS43108560-', 
#     'WSB43430301-', 'WSB43115301-', 'WSB43523301-', 'WSB43523347-', 'WSB43123301-', 'WSB43123347-', 'WSB43530301-', 'WSB43530347-', 'WSB43130301-', 'WSB43130347-', 'WSB43140347-', 'WSB43149347-', 'WSB43162347-', 'WSB43423301-', 'WSB43730301-', 
# ]


VaillantPartsArticles = [
    '0010025841', '0020044776', '0020044790', '0020010717', '0020034951', '0020200682', '0020211606', '0010025882', '0020200660', '0020034055', '0020035010', '0020039184', '0020056517', '0020094636', '0020097207', '0020118696', '0020118741', '0020033963', '0020033966',
    '0010027587', '0020097214', '0020118640', '0020199915', '0020199930', '0010030668', '0010032760', '0020094635', '0020119604', '0010025874', '0010025877', '0010025880', '0010038073', '0020038356', '0020049374', '0020049376', '0020097962', '0020119390', '0020120239',
    '0020154085', '0020200395', '0020254535', '0020260655', '0020014175', '0020033474', '0020033476', '0020033993', '0020035066', '0020118623', '0020118708', '0020118737', '0020195512', '0020195522', '0020056464', '0020098253', '0020200681', '0020059452', '0020094645',
    '0010025847', '0010045925', '0020118703', '0020094646', '0020094647', '0020094648', '0020025301', '0020027504', '0020027505', '0020027508', '0020033250', '0020118686', '0020195525', '0020200638', '0020253011', '0020025267', '0020046737', '0020048749', '0020027634',
    '0020197548', '0020052480', '0010026210', '0020200599', '0020033908', '0020049378', '0020033981', '0020120233', '0020142414', '0020211624', '0020035407', '0020027519', '0020025264'
]

analogue = []
articles = ['0010025841']

for article in articles:
    product = saveProduct(dbObj, article)
    events = []
    events = saveEvents(dbObj, product)
    if len(events):
        calculateHistoricStock(dbObj, product, events)
    print(f"Article {article} processed")

dbObj.closeConnection()
