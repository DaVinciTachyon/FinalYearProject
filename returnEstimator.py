from priceGatherer import getPrices
from sentimentExtractor import getArticleSentimentByDate
import pandas as pd

def getPricesExcel():
    import pandas as pd
    import json
    dataFrame = pd.read_json(json.dumps(getPrices()))
    dataFrame.to_excel('prices.xlsx')

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

def equalDate(dateA, dateB):
    dtA = getDateTime(dateA)
    dtB = getDateTime(dateB)
    return dtA == dtB

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

    colours = ["b", "g", "r", "c", "m", "y", "k", "w"]
    colourN = 0
    fontSize = 11

    fig, ax = plt.subplots()
    for f in pricesFrames:
        ax.plot(f, color=colours[colourN], marker="o")
        colourN += 1
    ax.set_xlabel("date", fontsize=fontSize)
    ax.set_ylabel("price", fontsize=fontSize)

    ax2 = ax.twinx()
    for f in sentimentFrames:
        ax2.plot(f, color=colours[colourN], marker="o")
        colourN += 1
    ax2.set_ylabel("sentiment", fontsize=fontSize)

    legend = []
    for p in pricesColumns:
        legend.append(p)
    for s in sentimentColumns:
        legend.append(s)
    fig.legend(legend)

    plt.show()
    fig.savefig('priceVsSentiment.jpg',
                format='jpeg',
                dpi=100,
                bbox_inches='tight')
    
def getInOutSeries(prices, sentiment, pricesColumns, sentimentColumns):
    inp = []
    outp = []
    i = 0
    for s in sentiment:
        date = s['date']
        entry = []
        for sC in sentimentColumns:
            entry.append(s[sC])
        pEntry = {}
        for p in range(i, len(prices)):
            if(pricesColumns[0] in pEntry and greaterThanDate(prices[p]['date'], date)):
                for pC in pricesColumns:
                    entry.append(pEntry[pC])
                outp.append(prices[p]['close'] > prices[p - 1]['close'])
                break
            elif(equalDate(prices[p]['date'], date)):
                for pC in pricesColumns:
                    entry.append(prices[p][pC])
                outp.append(prices[p + 1]['close'] > prices[p]['close'])
                break
            for pC in pricesColumns:
                pEntry[pC] = prices[p][pC]
            i += 1
        inp.append(entry)
    return inp, outp
                
def singlePointEstimator(prices, sentiment, pricesColumns, sentimentColumns): # TODO use more models
    prices, sentiment = getDisplaySeries(prices, sentiment)
    X, y = getInOutSeries(prices, sentiment, pricesColumns, sentimentColumns)
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import KFold
    from sklearn.metrics import accuracy_score
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.utils import shuffle
    X = np.array(X)
    y = np.array(y)
    X, y = shuffle(X, y)
    K = range(1, 10)
    highestAccuracy = 0
    highestAccuracyK = None
    for k in K:
        kf = KFold(n_splits=2)
        accuracies = []
        for train, test in kf.split(X):
            model = KNeighborsClassifier(n_neighbors=k).fit(X[train], y[train])
            pY = model.predict(X[test])
            accuracies.append(accuracy_score(y[test], pY))
        accuracies = np.array(accuracies)
        accuracy = np.mean(accuracies)
        if(accuracy > highestAccuracy):
            highestAccuracy = accuracy
            highestAccuracyK = k
    
    model = KNeighborsClassifier(n_neighbors=highestAccuracyK).fit(X, y)
    return model, highestAccuracy

sentiment = getArticleSentimentByDate()
prices = getPrices()

def getNextDayReturn(prices, sentiment):
    import numpy as np
    
    s = []
    x = []
    y = []
    j = 0
    for i in range(1, len(prices) - 1):
        while(j < len(sentiment) and greaterThanDate(prices[i]['date'], sentiment[j]['date'])):
            j += 1
        if(j < len(sentiment) and equalDate(sentiment[j]['date'], prices[i]['date'])):
            s.append(sentiment[j]['negativeSentiment'])
        else:
            s.append(0)
        x.append(prices[i]['return1Day'])
        y.append(prices[i + 1]['return1Day'])
    lastSentiment = s[len(s) - 1]
    lastReturn = y[len(y) - 1]
    returnsCorr = np.corrcoef(x, y)[0][1]
    sentimentCorr = np.corrcoef(s, y)[0][1]
    x.append(lastReturn)
    mean = np.mean(x)

    error = 0 # FIXME currently assuming normally distributed
    return mean + returnsCorr * lastReturn + sentimentCorr * lastSentiment + error

# getPricesExcel()
# displayGraphs(prices, sentiment, ['return1Day'], ['negativeSentiment'])
# sModel, sAccuracy = singlePointEstimator(prices, sentiment, ['return1Day'], ['negativeSentiment', 'positiveSentiment'])
# print(sAccuracy)
print(getNextDayReturn(prices, sentiment))
