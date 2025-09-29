from constants import *
import requests
import datetime
from moyskladConnection import moySkaldConnection

class Product(moySkaldConnection):
    def get(self, article, attributes):
        productUrl  = f'https://api.moysklad.ru/api/remap/1.2/entity/product?filter=article={article}&fields=minimumStock'

        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }

        response = requests.request("GET", productUrl, headers=headers, data=payload)
        resonseJson = response.json()
        if not len(resonseJson['rows']):
            print("No products found")
            return {}
        elif len(resonseJson['rows']) > 1:
            print('More than one product found')
            return {}
        else:
            return self.buildProduct(resonseJson['rows'][0], attributes)

    def buildProduct(self, receivedProduct, expectedAttributes):
        newProduct = {}
        for attribute in expectedAttributes:
            match attribute:
                case "demandFilterUrl":
                    pass
                case "supplyFilterUrl":
                    pass
                case "lastSyncDate":
                    x = datetime.datetime.now()
                    newProduct[attribute] = x.strftime(DATE_TIME_FORMAT)
                case "minimumStock":
                    newProduct[attribute] = receivedProduct[attribute]["quantity"]
                case _:
                    newProduct[attribute] = receivedProduct[attribute]
        return newProduct
    
    def getFilterUrl(self, article, filterType):
        match filterType:
            case "demand":
                pass
            case "supply":
                pass
            case _:
                raise Exception("Filter type not recognised")

        demandFilterUrl = f"https://api.moysklad.ru/api/remap/1.2/entity/{filterType}/namedfilter"

        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }

        response = requests.request("GET", demandFilterUrl, headers=headers, data=payload)
        resonseJson = response.json()

        if not len(resonseJson['rows']):
            print("No filters found")
            return None
        
        for filter in resonseJson['rows']:
            if filter['name'] == article:
                return filter['meta']['href']

        return None