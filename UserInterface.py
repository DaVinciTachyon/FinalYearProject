from priceGatherer import getPrices, addReturns
from sentimentExtractor import getArticleSentimentByDate, setSource, getZScores
from dataGraphing import displayPriceVsSentiment, displayHist
from dataTabling import getExcel
from dataCleanUp import getOverlappingSeries
from returnEstimator import singlePointEstimator
from correlation import getAutoCorrelationWithLags, getReturnSentimentCorrelations
from descriptiveStatistics import getDescriptiveStatistics
from dateUtil import getDashedDateTime, subtractYears, greaterThanOrEqualDate, toString

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
            "1: Return Vs Sentiment Grapher",
            "2: Single Point Estimator",
            "3: Autocorrelator",
            "4: Return Vs Sentiment Correlator",
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
            getReturnVsSentimentGrapherMenu(pV, sV, oPV, oSV)
        elif tool == 2:
            getSinglePointEstimatorMenu(oPV, oSV)
        elif tool == 3:
            getAutoCorrelatorMenu(pV, sV)
        elif tool == 4:
            getReturnVsSentimentCorrelatorMenu(oPV, oSV)
        elif tool == 5:
            getDescriptiveStatisticsMenu(pV, sV)
        elif tool == 6:
            getVectorAutoregressorMenu()
        elif tool == 7:
            getExcelMenu(pV, sV, oPV, oSV)
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

def createMenuFromKeys(name, keys):
    print(createMenuString(keys))
    columns = input(f"Please select {name} columns, separated by comma: ").split(",")
    numericColumns = []
    for i in range(len(columns)):
        columns[i] = columns[i].strip()
        if columns[i].isdigit():
            numericColumns.append(int(columns[i]))
    namedColumns = []
    for n in numericColumns:
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

def getReturnVsSentimentGrapherMenu(prices, sentiment, oPrices, oSentiment):
    print("Return Vs Sentiment Grapher")

    priceKeys = getPriceKeys(prices)
    priceColumns = createMenuFromKeys("price", priceKeys)
    
    sentimentKeys = getSentimentKeys(sentiment)
    sentimentColumns = createMenuFromKeys("sentiment", sentimentKeys)

    if len(priceColumns) > 0 and len(sentimentColumns) > 0:
        priceValues = oPrices
        sentimentValues = oSentiment
    else:
        priceValues = prices
        sentimentValues = sentiment

    displayPriceVsSentiment(priceValues, sentimentValues, priceColumns, sentimentColumns)

def getSinglePointEstimatorMenu(oPrices, oSentiment):
    # TODO Look at more models, get to choose?
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

def selectColumn(keys):
    selected = False
    while not selected:
        print(createMenuString(keys))
        column = input("Please select a column: ").strip()
        if column.isdigit():
            column = int(column)
        if isinstance(column, int) and column > 0 and column <= len(keys):
            column = keys[column - 1]
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
    for i in range(lag):
        correlation, lr = correlations[i]
        print(i + 1, "day lag", correlation)

def getReturnVsSentimentCorrelatorMenu(oPrices, oSentiment):
    print("Return Vs Sentiment Correlator")

    sameDayCorr, returnSentCorr, sentReturnCorr = getReturnSentimentCorrelations(oPrices, oSentiment)
    print("return1Day/negativeSentiment Correlation")
    correlation, lr = sameDayCorr
    print("same day", correlation)
    correlation, lr = returnSentCorr
    print("1 day lag return1Day to negativeSentiment", correlation)
    correlation, lr = sentReturnCorr
    print("1 day lag negativeSentiment to return1Day", correlation)

def getDescriptiveStatisticsMenu(prices, sentiment):
    keys, dataset, _ = selectDataset(prices, sentiment)
    columnName = selectColumn(keys)
    start = getStart(columnName)
    column = [dataset[i][columnName] for i in range(start, len(dataset))]
    getDescriptiveStatistics(column, columnName)
    displayHist(column, 100, columnName)

def getExcelMenu(prices, sentiment, oPrices, oSentiment):
    # TODO overlapping excel
    _, dataset, name = selectDataset(prices, sentiment)
    getExcel(dataset, f"{name}/{name}")

def getVectorAutoregressorMenu():
    print("Work In Progress")