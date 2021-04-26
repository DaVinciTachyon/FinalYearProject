import scipy.stats as stats
from dateUtil import greaterThanDate, equalDate

def getCorrelation(x, y):
    return stats.pearsonr(x, y)

def getCorrelationWithLag(array, column1, column2, start, lag):
    x = []
    y = []
    for j in range(start, len(array) - lag):
        x.append(array[j][column1])
        y.append(array[j + lag][column2])
    return getCorrelation(x, y)

def getAutoCorrelationWithLag(array, column, start, lag):
    return getCorrelationWithLag(array, column, column, start, lag)

def getAutoCorrelationWithLags(array, column, start, lag):
    i = 1
    corr = []
    while(i <= lag):
        corr.append(getAutoCorrelationWithLag(array, column, start, i))
        i += 1
    return corr

def getPriceSentimentCorrelations(prices, sentiment, priceColumn, sentimentColumn, lag, start):
    x = []
    y = []
    j = 0
    for i in range(start, len(prices)):
        x.append(prices[i][priceColumn])
        while(j < len(sentiment) and greaterThanDate(prices[i]['date'], sentiment[j]['date'])):
            j += 1
        if(j < len(sentiment) and equalDate(sentiment[j]['date'], prices[i]['date'])):
            if sentimentColumn == "posNeg":
                pos = sentiment[j]["positiveSentiment"]
                if pos == 0:
                    pos = 0.0000000000000001
                y.append(sentiment[j]["negativeSentiment"] / pos)
            else:
                y.append(sentiment[j][sentimentColumn])
        else:
            y.append(0)
    priceSentCorr = []
    sentpriceCorr = []
    for i in range(lag + 1):
        mi = -1 * i
        if i == 0:
            priceSentCorr.append(getCorrelation(x, y))
            sentpriceCorr.append(getCorrelation(x, y))
        else:
            priceSentCorr.append(getCorrelation(x[:mi], y[i:]))
            sentpriceCorr.append(getCorrelation(x[i:], y[:mi]))
    return priceSentCorr, sentpriceCorr

def getPriceCorrelations(prices, columnA, columnB, lag, start):
    x = []
    y = []
    for i in range(start, len(prices)):
        x.append(prices[i][columnA])
        y.append(prices[i][columnB])
    AtoB = []
    BtoA = []
    for i in range(lag + 1):
        mi = -1 * i
        if i == 0:
            AtoB.append(getCorrelation(x, y))
            BtoA.append(getCorrelation(x, y))
        else:
            AtoB.append(getCorrelation(x[:mi], y[i:]))
            BtoA.append(getCorrelation(x[i:], y[:mi]))
    return AtoB, BtoA