from priceGatherer import getPrices
from sentimentExtractor import getArticleSentimentByDate, setSource
from dataGraphing import displayPriceVsSentiment
from dataTabling import getExcel
from dataCleanUp import getOverlappingSeries
from returnEstimator import singlePointEstimator, getNextDayReturn
from correlation import getAutoCorrelationWithLags, getReturnSentimentCorrelations
from descriptiveStatistics import getDescriptiveStatistics

# determine all vars such as source here
# add zeros to overlapping
# store tidied data as json
# rtf to json and store

if __name__ == "__main__":
    source = "lexisnexis"
    # source = "proquest"

    setSource(source)
    sentiment = getArticleSentimentByDate()
    prices = getPrices()

    oPrices, oSentiment = getOverlappingSeries(prices, sentiment)

    getExcel(prices, 'prices/prices')
    displayPriceVsSentiment(oPrices, oSentiment, ['return1Day'], ['negativeSentiment'])
    # displayPriceVsSentiment(oPrices, oSentiment, ['return1Day'], ['articles'])
    # sModel, sAccuracy = singlePointEstimator(oPrices, oSentiment, ['close', 'high', 'low', 'openPrice', 'volume', 'return1Day', 'return7Day', 'return14Day', 'return21Day'], ['articles', 'totalWords', 'negativeSentiment', 'positiveSentiment'])
    # print(sAccuracy)
    # print(getNextDayReturn(oPrices, oSentiment))
    # returnsCorr = getAutoCorrelationWithLags(prices, 'return1Day', 1, 5)
    # print(returnsCorr)
    # priceCorr = getAutoCorrelationWithLags(prices, 'close', 0, 5)
    # print(priceCorr)
    # a, b, c = getReturnSentimentCorrelations(oPrices, oSentiment)
    # print(a)
    # print(b)
    # print(c)
    # returns = []
    # for i in range(1, len(prices)):
    #     returns.append(prices[i]['return1Day'])
    # getDescriptiveStatistics(returns, "1 Day Returns")
    # closingPrices = []
    # for p in prices:
    #     closingPrices.append(p['close'])
    # getDescriptiveStatistics(closingPrices, "Closing Prices")
    # negSentiment = []
    # for n in sentiment:
    #     negSentiment.append(n['negativeSentiment'])
    # getDescriptiveStatistics(negSentiment, "Negative Sentiment")