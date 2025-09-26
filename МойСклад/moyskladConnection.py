from constants import *
import requests
import base64
import datetime

class moySkaldConnection:
    def __init__(self):
        self.username = "johntheron@3323234"
        self.password = "TeExjsm$1QY@Qw"

    def getBasicAuth(self):
        token = base64.b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'
        
    def getSales(self, article, attributes):
        return []
        
