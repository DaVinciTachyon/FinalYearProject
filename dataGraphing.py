import matplotlib.pyplot as plt
import pandas as pd
from dataCleanUp import removeNoReturn

def getDataFrames(data, names):
    dates = []
    for d in data:
        dates.append(d['date'])
    dates = pd.to_datetime(dates)

    dataPoints = []
    for name in names:
        columnDataPoints = []
        for entry in data:
            columnDataPoints.append(entry[name])
        dataPoints.append(columnDataPoints)

    frames = []
    for i in range(len(names)):
        frames.append(pd.DataFrame(data=dataPoints[i], index=dates, columns=[names[i]]))

    return frames

def displayGraphs(prices, sentiment, pricesColumns, sentimentColumns):
    prices = removeNoReturn(prices, pricesColumns)
    pricesFrames = getDataFrames(prices, pricesColumns)
    sentimentFrames = getDataFrames(sentiment, sentimentColumns)

    colours = ["b", "g", "r", "c", "m", "y", "k", "w"]
    colourN = 0
    fontSize = 11

    fig, ax = plt.subplots()
    for f in pricesFrames:
        ax.plot(f, color=colours[colourN], marker="o")
        colourN += 1
    ax.set_xlabel("date", fontsize=fontSize)
    ax.set_ylabel("price", fontsize=fontSize)

    ax2 = ax.twinx()
    for f in sentimentFrames:
        ax2.plot(f, color=colours[colourN], marker="o")
        colourN += 1
    ax2.set_ylabel("sentiment", fontsize=fontSize)

    legend = []
    for p in pricesColumns:
        legend.append(p)
    for s in sentimentColumns:
        legend.append(s)
    fig.legend(legend)

    plt.show()
    fig.savefig('priceVsSentiment.jpg',
                format='jpeg',
                dpi=100,
                bbox_inches='tight')