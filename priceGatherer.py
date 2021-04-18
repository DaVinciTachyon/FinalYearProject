import os.path
import json
import requests
from dotenv import load_dotenv
import os
import math
import operator

pricesFilename = "./prices/prices.json"

def filterKeys(data):
    keys = [ 'date', 'close', 'symbol', 'volume' ]
    nData = []
    for entry in data:
        filteredEntry = {}
        for key in keys:
            filteredEntry[key] = entry[key]
        nData.append(filteredEntry)
    return nData

def addReturns(prices):
    returnLengths = [ 1, 7, 14, 21 ]
    for i in range(len(prices)):
        for l in returnLengths:
            if(i >= l):
                prices[i][f"return{l}Day"] = math.log(prices[i]['close']/prices[i-l]['close'])
    return prices

def getPrices():
    if os.path.isfile(pricesFilename):
        with open(pricesFilename) as json_file:
            data = json.load(json_file)
    else:
        load_dotenv()
        apiToken = os.environ.get("IEX_CLOUD_API_TOKEN")

        timing = "5y"

        URL = "https://cloud.iexapis.com/stable/stock/GME/chart/{}".format(timing)
        # /stock/GME/chart/max #paid
        PARAMS = { 'token': apiToken }
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()

        data = sorted(data, key = operator.itemgetter('date'))

        with open(pricesFilename, 'w') as json_file:
            json.dump(data, json_file)

    return filterKeys(data)