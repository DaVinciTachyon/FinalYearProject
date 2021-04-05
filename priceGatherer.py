import os.path
import json
import requests
from dotenv import load_dotenv
import os

pricesFilename = "./prices/prices.json"

def filterKeys(data):
    keys = [ 'date', 'close', 'high', 'low', 'open', 'symbol', 'volume' ]
    nData = []
    for entry in data:
        filteredEntry = {}
        for key in keys:
            if(key == 'open'):
                filteredEntry['openPrice'] = entry[key]
            else:
                filteredEntry[key] = entry[key]
        nData.append(filteredEntry)
    return nData

def addReturns(prices):
    import math
    returnLengths = [ 1, 7, 14, 21 ]
    for i in range(len(prices)):
        for l in returnLengths:
            if(i >= l):
                prices[i]["return{}Day".format(l)] = math.log(prices[i]['close']/prices[i-l]['close'])
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

        import operator
        data = sorted(data, key = operator.itemgetter('date'))

        with open(pricesFilename, 'w') as json_file:
            json.dump(data, json_file)

    return filterKeys(data)