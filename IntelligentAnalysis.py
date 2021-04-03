from priceGatherer import getPrices
from sentimentExtractor import getArticleSentimentByDate
from dataGraphing import displayPriceVsSentiment
from dataTabling import getExcel
from dataCleanUp import getOverlappingSeries
from returnEstimator import singlePointEstimator, getNextDayReturn
from correlation import getAutoCorrelationWithLags, getReturnSentimentCorrelations

if __name__ == "__main__": # determine all vars such as source here
    sentiment = getArticleSentimentByDate()
    prices = getPrices()

    prices, sentiment = getOverlappingSeries(prices, sentiment)

    # getExcel(prices, 'prices')
    # displayPriceVsSentiment(prices, sentiment, ['return1Day'], ['negativeSentiment'])
    displayPriceVsSentiment(prices, sentiment, ['return1Day'], ['articles'])
    # sModel, sAccuracy = singlePointEstimator(prices, sentiment, ['return1Day', 'return7Day', 'return14Day', 'return21Day'], ['negativeSentiment', 'positiveSentiment'])
    # print(sAccuracy)
    # print(getNextDayReturn(prices, sentiment))
    # returnsCorr = getAutoCorrelationWithLags(prices, 'return1Day', 1, 5)
    # print(returnsCorr)
    # priceCorr = getAutoCorrelationWithLags(prices, 'close', 0, 5)
    # print(priceCorr)
    # a, b, c = getReturnSentimentCorrelations(prices, sentiment)
    # print(a)
    # print(b)
    # print(c)