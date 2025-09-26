from constants import *
import requests
import base64
import datetime

username = "johntheron@3323234"
password = "TeExjsm$1QY@Qw"

def getBasicAuth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def getProduct(article, attributes):
    productUrl  = f'https://api.moysklad.ru/api/remap/1.2/entity/product?filter=article={article}&fields=minimumStock'

    payload = {}
    headers = {
        'Authorization': getBasicAuth(username, password)
    }

    response = requests.request("GET", productUrl, headers=headers, data=payload)
    resonseJson = response.json()
    if not len(resonseJson['rows']):
        print("no products found")
        return {}
    elif len(resonseJson['rows']) > 1:
        print('More than one product found')
        return {}
    else:
        return buildProduct(resonseJson['rows'][0], attributes)
    
def getSales(article, attributes):
    return []
    
def buildProduct(receivedProduct, expectedAttributes):
    newProduct = {}
    for attribute in expectedAttributes:
        match attribute:
            case "filterUrl":
                pass
            case "lastSyncDate":
                x = datetime.datetime.now()
                newProduct[attribute] = x.strftime(DATE_TIME_FORMAT)
            case "minimumStock":
                newProduct[attribute] = receivedProduct[attribute]["quantity"]
            case _:
                newProduct[attribute] = receivedProduct[attribute]
    return newProduct
        
