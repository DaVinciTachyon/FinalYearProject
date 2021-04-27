from priceGatherer import getPrices, addReturns
from sentimentExtractor import getArticleSentimentByDate, setSource, getZScores
from dataGraphing import displayPriceVsSentiment, displayHist
from dataTabling import getExcel
from dataCleanUp import getOverlappingSeries
from returnEstimator import singlePointEstimator
from correlation import getAutoCorrelationWithLags, getPriceSentimentCorrelations
from descriptiveStatistics import getDescriptiveStatistics
from dateUtil import getDashedDateTime, subtractYears, greaterThanOrEqualDate, toString
from VectorAutoregression import VAR

def getWelcomeMessage():
    print("This is an tool which aids in the analysis of return and sentiment relationships")

def UserInterface():
    getWelcomeMessage()
    setSource("lexisnexis")

    sentiment = getArticleSentimentByDate()
    prices = getPrices()

    oPrices, oSentiment = getOverlappingSeries(prices, sentiment)

    sentiment = getZScores(sentiment)
    oSentiment = getZScores(oSentiment)
    prices = addReturns(prices)
    oPrices = addReturns(oPrices)

    quit = False

    while not quit:
        print("Tool Selection")
        print(
            "1: Price Vs Sentiment Grapher",
            "2: Single Point Estimator",
            "3: Autocorrelator",
            "4: Price Vs Sentiment Correlator",
            "5: Descriptive Statistics",
            "6: Vector Autoregressor",
            "7: Create Excel Sheet"
            "8: Quit",
            sep="\t"
        )
        tool = input("Please select your tool: ").strip()
        if tool.isdigit():
            tool = int(tool)
        if isinstance(tool, int) and tool > 0 and tool < 8:
            print("1: 1 year", "2: 2 year", "3: 3 year", "4: maximum available", sep="\t")
            sampleSize = input("Please select the length of your sample size: ")
            if sampleSize.isdigit():
                sampleSize = int(sampleSize)
            if isinstance(sampleSize, int) and sampleSize > 0 and sampleSize < 4:
                pV, sV, oPV, oSV = selectPeriods(sampleSize, prices, sentiment, oPrices, oSentiment)
            else:
                pV, sV, oPV, oSV = prices, sentiment, oPrices, oSentiment
        if tool == 1:
            getPriceVsSentimentGrapherMenu(pV, sV, oPV, oSV)
        elif tool == 2:
            getSinglePointEstimatorMenu(oPV, oSV)
        elif tool == 3:
            getAutoCorrelatorMenu(pV, sV)
        elif tool == 4:
            getPriceVsSentimentCorrelatorMenu(oPV, oSV)
        elif tool == 5:
            getDescriptiveStatisticsMenu(pV, sV)
        elif tool == 6:
            getVectorAutoregressorMenu(oPV, oSV)
        elif tool == 7:
            getExcelMenu(oPV, oSV)
        elif tool == 8:
            quit = True
        else:
            print("Please try again\n")
    print("Thank you, goodbye")

def selectPeriods(period, prices, sentiment, oPrices, oSentiment):
    pV = selectPeriod(period, prices)
    sV = selectPeriod(period, sentiment)
    oPV = selectPeriod(period, oPrices)
    oSV = selectPeriod(period, oSentiment)
    return pV, sV, oPV, oSV

def selectPeriod(period, dataset):
    date = getDashedDateTime(dataset[len(dataset) - 1]['date'])
    startDate = subtractYears(date, period)
    nDataset = []
    for e in dataset:
        if greaterThanOrEqualDate(e["date"], toString(startDate)):
            nDataset.append(e)
    return nDataset

def createMenuString(elements):
    menuString = ""
    i = 1
    for p in elements:
        menuString += str(i) + ": " + p + "\t"
        i += 1
    return menuString

def getColumns(name, keys, posNeg = False):
    if posNeg:
        print(createMenuString(keys), f"{len(keys) + 1}: Positive to Negative Ratio")
    else:
        print(createMenuString(keys))
    columns = input(f"Please select {name} columns, separated by comma: ").split(",")
    numericColumns = []
    for i in range(len(columns)):
        columns[i] = columns[i].strip()
        if columns[i].isdigit():
            numericColumns.append(int(columns[i]))
    namedColumns = []
    for n in numericColumns:
        if n == len(keys) + 1:
            namedColumns.append("posNeg")
        else:
            namedColumns.append(keys[n - 1])
    return namedColumns

def getPriceKeys(prices):
    priceKeys = list(prices[len(prices) - 1].keys())
    priceKeys.remove("date")
    priceKeys.remove("symbol")
    return priceKeys

def getSentimentKeys(sentiment):
    sentimentKeys = list(sentiment[len(sentiment) - 1].keys())
    sentimentKeys.remove("date")
    return sentimentKeys

def getPriceVsSentimentGrapherMenu(prices, sentiment, oPrices, oSentiment):
    print("Price Vs Sentiment Grapher")

    priceKeys = getPriceKeys(prices)
    priceColumns = getColumns("price", priceKeys)
    
    sentimentKeys = getSentimentKeys(sentiment)
    sentimentColumns = getColumns("sentiment", sentimentKeys, True)

    if len(priceColumns) > 0 and len(sentimentColumns) > 0:
        priceValues = oPrices
        sentimentValues = oSentiment
    else:
        priceValues = prices
        sentimentValues = sentiment

    displayPriceVsSentiment(priceValues, sentimentValues, priceColumns, sentimentColumns)

def getSinglePointEstimatorMenu(oPrices, oSentiment):
    print("Single Point Estimator")

    priceKeys = getPriceKeys(oPrices)
    sentimentKeys = getSentimentKeys(oSentiment)
    model, accuracy = singlePointEstimator(oPrices, oSentiment, priceKeys, sentimentKeys)
    print("Model Name: ", model.__class__.__name__)
    print("Model Accuracy: ", accuracy)

def selectDataset(prices, sentiment):
    selected = False
    while not selected:
        print("1: Prices", "2: Sentiment", sep="\t")
        section = input("Select section to investigate: ")
        if section.isdigit():
            section = int(section)
        if section != 1 and section != 2:
            print("Please try again")
        else:
            selected = True
    if section == 1:
        dataset = prices
        keys = getPriceKeys(dataset)
        name = "prices"
    elif section == 2:
        dataset = sentiment
        keys = getSentimentKeys(dataset)
        name = "sentiment"
    return keys, dataset, name

def selectColumn(keys, posNeg = False):
    selected = False
    while not selected:
        if posNeg:
            print(createMenuString(keys), f"{len(keys) + 1}: Positive to Negative Ratio")
        else:
            print(createMenuString(keys))
        column = input("Please select a column: ").strip()
        if column.isdigit():
            column = int(column)
        if isinstance(column, int) and column > 0 and column <= len(keys):
            column = keys[column - 1]
            selected = True
        elif posNeg and isinstance(column, int) and column == len(keys) + 1:
            column = "posNeg"
            selected = True
        else:
            print("Please try again")
    return column

def selectLag():
    selected = False
    while not selected:
        lag = input("Please select lag length: ").strip()
        if lag.isdigit():
            lag = int(lag)
        if isinstance(lag, int) and lag > 0:
            selected = True
        else:
            print("Please try again")
    return lag

def getStart(column):
    start = 0
    if column.startswith("return"):
        start = int(column.lstrip("return").rstrip("Day"))
    return start

def getAutoCorrelatorMenu(prices, sentiment):
    print("Auto Correlator")

    keys, dataset, _ = selectDataset(prices, sentiment)
    column = selectColumn(keys)
    lag = selectLag()
    start = getStart(column)
    correlations = getAutoCorrelationWithLags(dataset, column, start, lag)
    print(f"{column} Auto Correlation")
    print("Lag", "Correlation", "P-Value", sep="\t")
    for i in range(lag):
        correlation, pValue = correlations[i]
        print(i + 1, round(correlation, 4), round(pValue, 4), sep="\t")

def getPriceVsSentimentCorrelatorMenu(oPrices, oSentiment):
    print("Price Vs Sentiment Correlator")

    priceKeys = getPriceKeys(oPrices)
    priceColumn = selectColumn(priceKeys)
    sentimentKeys = getSentimentKeys(oSentiment)
    sentimentColumn = selectColumn(sentimentKeys, True)
    lag = selectLag()
    start = getStart(priceColumn)
    priceSentCorr, sentPriceCorr = getPriceSentimentCorrelations(oPrices, oSentiment, priceColumn, sentimentColumn, lag, start)
    print(priceColumn, "Vs", sentimentColumn, "Correlation")
    print(f"& {priceColumn}/{sentimentColumn} & {sentimentColumn}/{priceColumn}", sep="\t")
    print("Lag", "Correlation", "P-Value", "Correlation", "P-Value", sep="\t")
    for i in range(len(priceSentCorr)):
        correlationA, pValueA = priceSentCorr[i]
        correlationB, pValueB = sentPriceCorr[i]
        print(i, round(correlationA, 4), round(pValueA, 4), round(correlationB, 4), round(pValueB, 4), sep="\t")

def getDescriptiveStatisticsMenu(prices, sentiment):
    keys, dataset, _ = selectDataset(prices, sentiment)
    columnName = selectColumn(keys)
    start = getStart(columnName)
    column = [dataset[i][columnName] for i in range(start, len(dataset))]
    getDescriptiveStatistics(column, columnName)
    displayHist(column, 100, columnName)

def getExcelMenu(prices, sentiment):
    dataset = []
    for i in range(len(prices)):
        dict = {}
        for (key, value) in prices[i].items():
            dict[key] = value
        for (key, value) in sentiment[i].items():
            dict[key] = value
        pos = dict["positiveSentiment"]
        if pos == 0:
            pos = 0.0000000000000001
        dict['posNeg'] = dict["negativeSentiment"] / pos
        dataset.append(dict)
    getExcel(dataset, "data")

def getVectorAutoregressorMenu(oPrices, oSentiment):
    priceKeys = getPriceKeys(oPrices)
    priceColumns = getColumns("price", priceKeys)
    
    sentimentKeys = getSentimentKeys(oSentiment)
    sentimentColumns = getColumns("sentiment", sentimentKeys, True)

    lag = selectLag()
    mainColumn = "return1Day"
    start = getStart(mainColumn)
    significance = 0.9

    correlation, pValue, mse, accuracy = VAR(oPrices, oSentiment, mainColumn, start, lag, priceColumns, sentimentColumns, significance)
    
    print("correlation:", correlation, "\tpValue:", pValue, "\tmse:", mse, "\taccuracy:", accuracy)