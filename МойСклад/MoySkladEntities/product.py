from constants import *
import requests
import datetime
from moyskladConnection import moySkaldConnection

class Product(moySkaldConnection):
    def __init__(self):
        self.limit = 1000
        super().__init__()

    def get(self, article, attributes):
        productUrl  = f'https://api.moysklad.ru/api/remap/1.2/entity/product?filter=article={article}&fields=minimumStock'

        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }

        response = requests.request("GET", productUrl, headers=headers, data=payload)
        resonseJson = response.json()
        if not len(resonseJson['rows']):
            raise Exception(f"No products found for article {article}")
        elif len(resonseJson['rows']) > 1:
            raise Exception(f"More than one product found: {article}")
        else:
            return self.build(resonseJson['rows'][0], attributes)
        
    def getArticlesByFilterName(self, filterId):
        productUrl  = f'https://api.moysklad.ru/api/remap/1.2/entity/product?namedfilter=https://api.moysklad.ru/api/remap/1.2/entity/product/namedfilter/{filterId}'

        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }
        articles = []
        offset = 0
        while True:
            urlWithLimit = productUrl + f"&offset={offset}&limit={self.limit}"
            response = requests.request("GET", urlWithLimit, headers=headers, data=payload)
            resonseJson = response.json()

            if not len(resonseJson['rows']):
                print(f"No products found at offset for filter {filterId}: {offset} limit: {self.limit}")
                return articles
            
            for product in resonseJson['rows']:
                if "article" not in product.keys():
                    print("No article found for: " + product['name'])
                    continue
                articles.append(product['article'])
            
            offset += self.limit

    def build(self, receivedProduct, expectedAttributes):
        newProduct = {}
        for attribute in expectedAttributes:
            match attribute:
                case "demandFilterUrl":
                    pass
                case "supplyFilterUrl":
                    pass
                case "lastCheckDate":
                    pass
                case "tgChatMentions":
                    pass
                case "RAT":
                    pass
                case "R12M":
                    pass
                case "R6M":
                    pass
                case "R3M":
                    pass
                case "riskStock":
                    pass
                case "category":
                    pathArray = receivedProduct['pathName'].split('/')
                    newProduct["category"] = pathArray[0] + "/" + pathArray[1]
                    pass
                case "brand":
                    for attributeInfo in receivedProduct['attributes']:
                        if attributeInfo['id'] == BRAND_FIELD_ID:
                            newProduct['brand'] = attributeInfo['value']
                    pass
                case "minimumStock":
                    if "minimumStock" in receivedProduct.keys():
                        newProduct[attribute] = receivedProduct[attribute]["quantity"]
                    else:
                        newProduct[attribute] = '0'
                    pass
                case "stock":
                    newProduct["stock"] = self.getStock(receivedProduct['article'])
                    pass
                case "cost":
                    dateNow = datetime.datetime.now()
                    dateFrom = str(int(dateNow.strftime(YEAR_FORMAT))-5) + "-" + dateNow.strftime(MONTH_FORMAT + "-" + DAY_FORMAT)
                    dateTo = dateNow.strftime(DATE_FORMAT)
                    x, cost = self.getPoints(receivedProduct['id'], dateFrom, dateTo)
                    if cost > 0:
                        newProduct["cost"] = cost
                    pass
                case "points":
                    dateNow = datetime.datetime.now()
                    dateFrom = str(int(dateNow.strftime(YEAR_FORMAT))-1) + "-" + dateNow.strftime(MONTH_FORMAT + "-" + DAY_FORMAT)
                    dateTo = dateNow.strftime(DATE_FORMAT)
                    newProduct["points"], x = self.getPoints(receivedProduct['id'], dateFrom, dateTo)
                    pass
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
    
    def getStock(self, article, log=False):
        dateNow = datetime.datetime.now()
        dateNow = dateNow.strftime(DATE_TIME_FORMAT)
        stockUrl = f"https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=article~{article};stockMoment={dateNow}"
        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }

        response = requests.request("GET", stockUrl, headers=headers, data=payload)
        resonseJson = response.json()

        if log:
            print(stockUrl)
            print(article, "stock left: ", resonseJson['rows'][0]['stock'])

        return resonseJson['rows'][0]['stock']
    
    def getPoints(self, productId, dateFrom, dateTo, log=False):
        profitUrl = f"https://api.moysklad.ru/api/remap/1.2/report/profit/byproduct?filter=product=https://api.moysklad.ru/api/remap/1.2/entity/product/{productId}&&momentFrom={dateFrom}&momentTo={dateTo}"

        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }
        response = requests.request("GET", profitUrl, headers=headers, data=payload)
        responseJson = response.json()

        if log:
            print(profitUrl)
            print(productId, "profit json: ", responseJson)

        if len(responseJson['rows']) == 0:
            return 0, 0
        return responseJson['rows'][0]['margin']*10, round(responseJson['rows'][0]['sellCost']/100, 2)

