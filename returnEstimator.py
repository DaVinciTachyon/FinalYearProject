import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from dataCleanUp import removeNoReturn
from dateUtil import greaterThanDate, equalDate
from correlation import getCorrelation

def getInOutSeries(prices, sentiment, pricesColumns, sentimentColumns):
    x = []
    y = []
    j = 0
    prices = removeNoReturn(prices, pricesColumns)
    for i in range(len(prices) - 1):
        entry = []
        for c in pricesColumns:
            entry.append(prices[i][c])
        while(j < len(sentiment) and greaterThanDate(prices[i]['date'], sentiment[j]['date'])):
            j += 1
        if(j < len(sentiment) and equalDate(sentiment[j]['date'], prices[i]['date'])):
            for c in sentimentColumns:
                entry.append(sentiment[j][c])
        else:
            for c in sentimentColumns:
                entry.append(0)
        x.append(entry)
        y.append(prices[i + 1]['close'] > prices[i]['close'])
    return x, y
                
def singlePointEstimator(prices, sentiment, pricesColumns, sentimentColumns): # TODO use more models
    X, y = getInOutSeries(prices, sentiment, pricesColumns, sentimentColumns)
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

def getNextDayReturn(prices, sentiment):    
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
    returnsCorr = getCorrelation(x, y)
    sentimentCorr = getCorrelation(s, y)
    x.append(lastReturn)
    mean = np.mean(x)

    error = 0 # FIXME currently assuming normally distributed
    return mean + returnsCorr * lastReturn + sentimentCorr * lastSentiment + error