from priceGatherer import getPrices, addReturns
from sentimentExtractor import getArticleSentimentByDate, setSource, getZScores
from dataGraphing import displayPriceVsSentiment, displayHist
from dataTabling import getExcel
from dataCleanUp import getOverlappingSeries
from returnEstimator import singlePointEstimator, getNextDayReturn
from correlation import getAutoCorrelationWithLags, getReturnSentimentCorrelations
from descriptiveStatistics import getDescriptiveStatistics

if __name__ == "__main__":
    source = "lexisnexis"
    # source = "proquest"

    setSource(source)
    sentiment = getArticleSentimentByDate()
    prices = getPrices()

    oPrices, oSentiment = getOverlappingSeries(prices, sentiment)

    sentiment = getZScores(sentiment)
    oSentiment = getZScores(oSentiment)
    prices = addReturns(prices)
    oPrices = addReturns(oPrices)

    # getExcel(prices, 'prices/prices')
    # displayPriceVsSentiment(oPrices, oSentiment, ['return1Day'], ['negativeSentiment'])
    # displayPriceVsSentiment(oPrices, oSentiment, ['return1Day'], ['articles'])
    # sModel, sAccuracy = singlePointEstimator(oPrices, oSentiment, ['close', 'volume', 'return1Day', 'return7Day', 'return14Day', 'return21Day'], ['articles', 'totalWords', 'negativeSentiment', 'positiveSentiment'])
    # print(sAccuracy)
    # print(getNextDayReturn(oPrices, oSentiment))
    # lag = 5
    # returnsCorr = getAutoCorrelationWithLags(prices, 'return1Day', 1, lag)
    # print("Returns Correlation")
    # for i in range(lag):
    #     print(i + 1, "day lag", returnsCorr[i])
    # priceCorr = getAutoCorrelationWithLags(prices, 'close', 0, lag)
    # print("Prices Correlation")
    # for i in range(lag):
    #     print(i + 1, "day lag", priceCorr[i])
    # sameDayCorr, returnSentCorr, sentReturnCorr = getReturnSentimentCorrelations(oPrices, oSentiment)
    # print("Return/Sentiment Correlation")
    # print("same day", sameDayCorr)
    # print("return to sentiment", returnSentCorr)
    # print("sentiment to return", sentReturnCorr)
    returns = []
    for i in range(1, len(prices)):
        returns.append(prices[i]['return1Day'])
    getDescriptiveStatistics(returns, "1 Day Returns")
    displayHist(returns, 100, "1 day returns")
    closingPrices = []
    for p in prices:
        closingPrices.append(p['close'])
    getDescriptiveStatistics(closingPrices, "Closing Prices")
    displayHist(closingPrices, 100, "closing prices")
    negSentiment = []
    for n in sentiment:
        negSentiment.append(n['negativeSentiment'])
    getDescriptiveStatistics(negSentiment, "Negative Sentiment")
    displayHist(negSentiment, 100, "negative sentiment")