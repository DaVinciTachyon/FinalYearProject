# The price gatherer gathers stock prices and changes for the company being analysed.
# It will use lexis nexis in order to gather the required information.
# It will then manipulate it to fit the requirements.

pricesFilename = "prices.json"

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

        with open(pricesFilename, 'w') as json_file:
            json.dump(data, json_file)

    return data

def getPricesExcel():
    import pandas as pd
    dataFrame = pd.read_json(pricesFilename)
    keys = [ 'close', 'high', 'low', 'open', 'symbol', 'volume' ]
    dataFrame = dataFrame[keys]
    dataFrame.to_excel('prices.xlsx')

getPrices()
getPricesExcel()