pricesFilename = "prices.json"

def filterKeys(data):
    keys = [ 'date', 'close', 'high', 'low', 'open', 'symbol', 'volume' ]
    nData = []
    for entry in data:
        filteredEntry = {}
        for key in keys:
            filteredEntry[key] = entry[key]
        nData.append(filteredEntry)
    return nData

def getPrices():
    import os.path
    import json

    if os.path.isfile(pricesFilename):
        with open(pricesFilename) as json_file:
            data = json.load(json_file)
    else:
        import requests
        from dotenv import load_dotenv
        import os

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

def getPricesExcel():
    import pandas as pd
    dataFrame = pd.read_json(getPrices())
    dataFrame.to_excel('prices.xlsx')