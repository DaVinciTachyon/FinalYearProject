from dateUtil import greaterThanDate, greaterThanOrEqualDate, equalDate

def removeNoReturn(prices, pricesColumns):
    lag = 0
    for p in pricesColumns:
        if "return" in p and "Day" in p:
            newLag = int(p.split("return")[1].split("Day")[0])
            if newLag > lag:
                lag = newLag
    return prices[lag:]

def getOverlap(prices, sentiment):
    sentStart = priceStart = 0
    sentEnd = priceEnd = None
    if(greaterThanDate(sentiment[0]['date'], prices[0]['date'])):
        while greaterThanDate(sentiment[0]['date'], prices[priceStart]['date']):
            priceStart += 1
    elif(greaterThanDate(prices[0]['date'], sentiment[0]['date'])):
        while greaterThanDate(prices[0]['date'], sentiment[sentStart]['date']):
            sentStart += 1
    if(greaterThanDate(sentiment[-1]['date'], prices[-1]['date'])):
        sentEnd = -1
        while greaterThanDate(sentiment[sentEnd]['date'], prices[-1]['date']):
            sentEnd -= 1
        sentEnd += 1
    elif(greaterThanDate(prices[-1]['date'], sentiment[-1]['date'])):
        priceEnd = -1
        while greaterThanDate(prices[priceEnd]['date'], sentiment[-1]['date']):
            priceEnd -= 1
        priceEnd += 1
    return prices[priceStart:priceEnd], sentiment[sentStart:sentEnd]

def getOverlappingSeries(prices, sentiment):
    prices, sentiment = getOverlap(prices, sentiment)
    i = 0
    while len(prices) != len(sentiment):
        if(greaterThanDate(sentiment[i]['date'], prices[i]['date'])):
            sentiment.insert(i, {'date': prices[i]['date'], 'articles': 0, 'totalWords': 0, 'positiveSentiment': 0, 'negativeSentiment': 0})
        elif(greaterThanDate(prices[i]['date'], sentiment[i]['date'])):
            prices.insert(i, {'date': sentiment[i]['date'], 'close': prices[i - 1]['close'], 'symbol': prices[i]['symbol'], 'volume': 0})
        else:
            i += 1
    return prices, sentiment