from correlation import getAutoCorrelationWithLags, getPriceSentimentCorrelations, getPriceCorrelations, getCorrelation
from dataGraphing import plot
import numpy as np

def VAR(prices, sentiment, mainColumn, start, lag, priceColumns, sentimentColumns, significance):
    # assumption that main column is 1 day returns
    priceCorrs = []
    for column in priceColumns:
        if mainColumn == column:
            corrs = getAutoCorrelationWithLags(prices, mainColumn, start, lag)
            priceCorrs.append((column, getSignificantEntries(corrs, significance, 1)))
        else:
            _, corrs = getPriceCorrelations(prices, mainColumn, column, lag, start)
            priceCorrs.append((column, getSignificantEntries(corrs, significance, 0)))
    sentimentCorrs = []
    for column in sentimentColumns:
        _, corrs = getPriceSentimentCorrelations(prices, sentiment, mainColumn, column, lag, start)
        sentimentCorrs.append((column, getSignificantEntries(corrs, significance, 0)))

    predictions = predict(mainColumn, priceCorrs, sentimentCorrs, prices, sentiment, lag, start)
    returns = []
    for i in range(start + lag, len(prices)):
        returns.append(prices[i]['return1Day'])
    correlation, pvalue = getCorrelation(returns, predictions)
    from sklearn.metrics import mean_squared_error, accuracy_score
    mse = mean_squared_error(returns, predictions)
    plot(returns, predictions, ["1 day returns", "predictions"])
    aReturns = []
    for r in returns:
        aReturns.append(r > 0)
    aPredictions = []
    for p in predictions:
        aPredictions.append(p > 0)
    accuracy = accuracy_score(aReturns, aPredictions)
    return correlation, pvalue, mse, accuracy

def predict(mainColumn, priceCorrs, sentimentCorrs, prices, sentiment, lag, start):
    column = []
    for i in range(start, len(prices)):
        column.append(prices[i][mainColumn])
    mainColumnMean = np.mean(column)
    predictions = []
    for i in range(start + lag, len(prices)):
        prediction = mainColumnMean
        for p in priceCorrs:
            name, values = p
            for v in values:
                lag, coef = v
                prediction += coef * prices[i - lag][name]
        for s in sentimentCorrs:
            name, values = s
            pPred = 0
            for v in values:
                lag, coef = v
                prediction += coef * sentiment[i - lag][name]
        predictions.append(prediction)
    return predictions

def getSignificantEntries(corrs, significance, start):
    i = start
    newCorrs = []
    for a in corrs:
        corr, p = a
        if p <= 1 - significance and i > 0:
            newCorrs.append((i, corr))
        i += 1
    return newCorrs