import numpy as np
from dateUtil import greaterThanDate, equalDate

def getCorrelation(x, y):
    return np.corrcoef(x, y)[0][1]

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

def getReturnSentimentCorrelations(prices, sentiment):
    x = []
    y = []
    j = 0
    for i in range(1, len(prices)):
        x.append(prices[i]['return1Day'])
        while(j < len(sentiment) and greaterThanDate(prices[i]['date'], sentiment[j]['date'])):
            j += 1
        if(j < len(sentiment) and equalDate(sentiment[j]['date'], prices[i]['date'])):
            y.append(sentiment[j]['negativeSentiment'])
        else:
            y.append(0)
    sameDayCorr = getCorrelation(x, y)
    returnSentCorr = getCorrelation(x[:-1], y[1:])
    sentReturnCorr = getCorrelation(x[1:], y[:-1])
    return sameDayCorr, returnSentCorr, sentReturnCorr