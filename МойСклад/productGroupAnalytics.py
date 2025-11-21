from constants import *
from mysqlConnection import mySqlConnection
import datetime

dbObj = mySqlConnection()
brand = BRAND_VAILLANT
categories = "'" + "','".join(VAILLANT_PARTS_CATEGORIES) + "'"
condition = f"""
                brand='{brand}' 
                AND category IN ({categories})
            """
attributes = dbObj.getEntityAttributes('product')
products = dbObj.getEntries('product', attributes, condition)


dateNow = datetime.datetime.now()
dateNow = dateNow.strftime(DATE_FORMAT)

financials = {
    "moment": dateNow, 
    "brand":brand, 
    "category": '"' + ",".join(VAILLANT_PARTS_CATEGORIES) + '"',
    "primeStockValue": 0,
    "riskStockValue": 0,
    "extraStockValue": 0,
    "targetPrimeStockValue": 0,
    "targetRiskStockValue": 0
    }
for i in range(len(products)):
# for i in range(4):
    product = products[i]
    if (product['stock'] is None or product['stock'] == 0) and (product['minimumStock'] is None or product['minimumStock']==0):
        print("no stock, no minimum stock")
        continue

    if product['cost'] == 0:
        raise Exception("Product " + product['article'] + " has no cost populated")
    print("product", product['article'])
    riskStock = (0 if product['riskStock'] is None else product['riskStock'])
    if  product['R3M'] is None:
        continue
    if "A" in product['R3M']:
        financials['targetPrimeStockValue'] += (product['minimumStock'] - riskStock)*product['cost']
        financials['targetRiskStockValue'] += riskStock*product['cost']
        if product['stock'] >= product['minimumStock'] - riskStock:
            financials['primeStockValue'] += (product['minimumStock'] - riskStock)*product['cost']
            financials['riskStockValue'] += min(riskStock, product['stock'] - (product['minimumStock'] - riskStock))*product['cost']

        if product['stock'] < product['minimumStock'] - riskStock:
            financials['primeStockValue'] += product['stock']*product['cost']

        if product['stock'] > product['minimumStock']:
            financials['extraStockValue'] += (product['stock'] - product['minimumStock'])*product['cost']

    elif "B" in product['R3M']:
        financials['targetRiskStockValue'] += product['minimumStock']*product['cost']
        if product['stock'] > product['minimumStock']:
            financials['riskStockValue'] += product['minimumStock']*product['cost']
            financials['extraStockValue'] += (product['stock'] - product['minimumStock'])*product['cost']
        else:
            financials['riskStockValue'] += product['stock']*product['cost']

    elif "C" in product['R3M']:
        print("category C")
        financials['extraStockValue'] += product['stock']*product['cost']

    print("financials", financials)

dbObj.saveEntity('financials', financials.keys(), financials, True, True)
dbObj.closeConnection()