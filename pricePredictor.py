# The predictor then gathers the output from the previous to sections 
# and uses a machine learning model in order to create a prediction for the market.
# I am originally considering it to be a simply up/down predictor, however,
# there is room for expansion, in the sense of predicting the size of the shift,
# as well as determining what timeframe it may be done in.
# This is a classification problem, therefore the scope of models that may be used is limited.
# The one suggested in most papers I have read about the topic is the kNN classifier, however,
# I will explore and compare various options such as logistic regression, decision trees, etc.

# input: [{date, active, negative, passive, positive, political, strong, weak, sentiment, topic}] - today price
# output: price direction - future price

from priceGatherer import getPrices, addReturns
from sentimentExtractor import getArticleSentimentByDate
import pandas as pd

def getPricesExcel():
    prices = addReturns(getPrices())
    import pandas as pd
    import json
    dataFrame = pd.read_json(json.dumps(prices))
    dataFrame.to_excel('prices.xlsx')

def VAR():
    print('hi')

def getDateTime(date):
    import datetime
    y, m, d = [int(x) for x in date.split('-')]
    return datetime.datetime(y, m, d)

def greaterThanDate(dateA, dateB):
    dtA = getDateTime(dateA)
    dtB = getDateTime(dateB)
    return dtA > dtB

def greaterThanOrEqualDate(dateA, dateB):
    dtA = getDateTime(dateA)
    dtB = getDateTime(dateB)
    return dtA >= dtB

def getDisplaySeries(prices, sentiment):
    if(greaterThanDate(sentiment[0]['date'], prices[0]['date'])):
        newPrices = []
        for price in prices:
            if(greaterThanOrEqualDate(price['date'], sentiment[0]['date'])):
                newPrices.append(price)
        prices = newPrices
    else:
        newSentiment = []
        for s in sentiment:
            if(greaterThanOrEqualDate(s['date'], prices[0]['date'])):
                newSentiment.append(s)
        sentiment = newSentiment
    return prices, sentiment

def getDataFrames(data, names):
    dates = []
    for d in data:
        dates.append(d['date'])
    dates = pd.to_datetime(dates)

    dataPoints = []
    for name in names:
        columnDataPoints = []
        for entry in data:
            columnDataPoints.append(entry[name])
        dataPoints.append(columnDataPoints)

    frames = []
    for i in range(len(names)):
        frames.append(pd.DataFrame(data=dataPoints[i], index=dates, columns=[names[i]]))

    return frames

def displayGraphs(prices, sentiment, pricesColumns, sentimentColumns):
    prices, sentiment = getDisplaySeries(prices, sentiment)

    pricesFrames = getDataFrames(prices, pricesColumns)
    sentimentFrames = getDataFrames(sentiment, sentimentColumns)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    for f in pricesFrames:
        ax.plot(f, color="red", marker="o")
    ax.set_xlabel("date", fontsize=11)
    ax.set_ylabel("price", color="red", fontsize=11)

    ax2 = ax.twinx()
    for f in sentimentFrames:
        ax2.plot(f, color="blue", marker="o")
    ax2.set_ylabel("sentiment", color="blue", fontsize=11)
    plt.show()
    # fig.savefig('priceVsSentiment.jpg',
    #             format='jpeg',
    #             dpi=100,
    #             bbox_inches='tight')

sentiment = getArticleSentimentByDate()
prices = getPrices()

# getPricesExcel()
# VAR()
displayGraphs(prices, sentiment, ['close'], ['negativeSentiment', 'positiveSentiment'])
