import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from dataCleanUp import removeNoReturn
from dateUtil import greaterThanDate, equalDate
from correlation import getCorrelation
import warnings
from time import perf_counter

warnings.filterwarnings("ignore")

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
        y.append(prices[i + 1]['return1Day'] > 0)
    return x, y
                
def singlePointEstimator(prices, sentiment, pricesColumns, sentimentColumns):
    X, y = getInOutSeries(prices, sentiment, pricesColumns, sentimentColumns)
    X = np.array(X)
    y = np.array(y)
    X, y = shuffle(X, y)
    highestAccuracy = 0
    highestAccuracyModel = None
    kf = KFold(n_splits=2)

    startTime = perf_counter()
    K = range(1, 10)
    highestAccuracyK = 0
    highestKNNAccuracy = 0
    for k in K:
        accuracies = []
        for train, test in kf.split(X):
            model = KNeighborsClassifier(n_neighbors=k).fit(X[train], y[train])
            pY = model.predict(X[test])
            accuracies.append(accuracy_score(y[test], pY))
        accuracies = np.array(accuracies)
        accuracy = np.mean(accuracies)
        if(accuracy > highestKNNAccuracy):
            highestKNNAccuracy = accuracy
            highestAccuracyK = k
    if(highestKNNAccuracy > highestAccuracy):
        highestAccuracy = highestKNNAccuracy
        highestAccuracyModel = KNeighborsClassifier(n_neighbors=highestAccuracyK).fit(X, y)
    print("Processed: ", model.__class__.__name__)
    print("Time: ", round((perf_counter() - startTime) * 1000), "ms")

    startTime = perf_counter()
    accuracies = []
    for train, test in kf.split(X):
        model = DecisionTreeClassifier().fit(X[train], y[train])
        pY = model.predict(X[test])
        accuracies.append(accuracy_score(y[test], pY))
    accuracies = np.array(accuracies)
    decisionTreeAccuracy = np.mean(accuracies)
    if(decisionTreeAccuracy > highestAccuracy):
        highestAccuracy = decisionTreeAccuracy
        highestAccuracyModel = DecisionTreeClassifier().fit(X, y)
    print("Processed: ", model.__class__.__name__)
    print("Time: ", round((perf_counter() - startTime) * 1000), "ms")

    startTime = perf_counter()
    accuracies = []
    kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0))
    for train, test in kf.split(X):
        model = GaussianProcessClassifier(kernel).fit(X[train], y[train])
        pY = model.predict(X[test])
        accuracies.append(accuracy_score(y[test], pY))
    accuracies = np.array(accuracies)
    gaussianProcessAccuracy = np.mean(accuracies)
    if(gaussianProcessAccuracy > highestAccuracy):
        highestAccuracy = gaussianProcessAccuracy
        highestAccuracyModel = GaussianProcessClassifier(kernel).fit(X, y)
    print("Processed: ", model.__class__.__name__)
    print("Time: ", round((perf_counter() - startTime) * 1000), "ms")

    startTime = perf_counter()
    accuracies = []
    for train, test in kf.split(X):
        model = AdaBoostClassifier().fit(X[train], y[train])
        pY = model.predict(X[test])
        accuracies.append(accuracy_score(y[test], pY))
    accuracies = np.array(accuracies)
    adaBoostAccuracy = np.mean(accuracies)
    if(adaBoostAccuracy > highestAccuracy):
        highestAccuracy = adaBoostAccuracy
        highestAccuracyModel = AdaBoostClassifier().fit(X, y)
    print("Processed: ", model.__class__.__name__)
    print("Time: ", round((perf_counter() - startTime) * 1000), "ms")

    startTime = perf_counter()
    N = range(1, 20)
    highestAccuracyN = 0
    highestRandomForestAccuracy = 0
    for n in N:
        accuracies = []
        for train, test in kf.split(X):
            model = RandomForestClassifier(n_estimators=n).fit(X[train], y[train])
            pY = model.predict(X[test])
            accuracies.append(accuracy_score(y[test], pY))
        accuracies = np.array(accuracies)
        accuracy = np.mean(accuracies)
        if(accuracy > highestRandomForestAccuracy):
            highestRandomForestAccuracy = accuracy
            highestAccuracyN = n
    if(highestRandomForestAccuracy > highestAccuracy):
        highestAccuracy = highestRandomForestAccuracy
        highestAccuracyModel = RandomForestClassifier(n_estimators=highestAccuracyN).fit(X, y)
    print("Processed: ", model.__class__.__name__)
    print("Time: ", round((perf_counter() - startTime) * 1000), "ms")
    
    return highestAccuracyModel, highestAccuracy