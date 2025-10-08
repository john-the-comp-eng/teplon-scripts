from constants import *
import requests
import datetime
from moyskladConnection import moySkaldConnection

class Event(moySkaldConnection):
    def __init__(self, eventType, product):
        self.eventType = eventType
        self.product = product
        self.limit = 100
        super().__init__()

    def get(self, attributes):
        filter = ""
        filterAttribute = self.eventType + "FilterUrl"
        if self.product[filterAttribute]:
            filter = "namedfilter=" + self.product[filterAttribute]
        if len(filter) == 0:
            raise Exception("Cannot retrieve event without a filter for article " + self.product['article'])
        eventUrl = f"https://api.moysklad.ru/api/remap/1.2/entity/{self.eventType}?expand=positions.assortment&{filter}"

        payload = {}
        headers = {
            'Authorization': self.getBasicAuth()
        }
        
        events = []
        offset = 0
        while True:
            urlWithLimit = eventUrl + f"&offset={offset}&limit={self.limit}"
            response = requests.request("GET", urlWithLimit, headers=headers, data=payload)
            resonseJson = response.json()

            if not len(resonseJson['rows']):
                print(f"No {self.eventType} events found at offset: {offset} limit: {self.limit}")
                return events
            
            for skladEvent in resonseJson['rows']:
                for soldProduct in skladEvent['positions']['rows']:
                        if soldProduct['assortment']['id'] == self.product['id']:
                            events.append(self.build(skladEvent, attributes))
            
            offset += self.limit

    def build(self, receivedEvent, expectedAttributes):
        newEvent = {}
        for attribute in expectedAttributes:
            match attribute:
                case "eventType":
                    newEvent[attribute] = self.eventType
                    pass
                case "product":
                    newEvent[attribute] = self.product["id"]
                    pass
                case "stock":
                    pass
                case "quantity":
                    newEvent[attribute] = 0
                    for soldProduct in receivedEvent['positions']['rows']:
                        if soldProduct['assortment']['id'] == self.product['id']:
                            newEvent[attribute] += soldProduct[attribute]
                            # 00114 supply is a test to make sure we count the quantity correctly
                    pass
                case _:
                    newEvent[attribute] = receivedEvent[attribute]
        return newEvent