from dateUtil import greaterThanDate, greaterThanOrEqualDate

def removeNoReturn(prices, pricesColumns):
    lag = 0
    for p in pricesColumns:
        if "return" in p and "Day" in p:
            newLag = int(p.split("return")[1].split("Day")[0])
            if newLag > lag:
                lag = newLag
    return prices[lag:]

def getOverlappingSeries(prices, sentiment): # FIXME add zeros to overlapping
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