import matplotlib.pyplot as plt
import pandas as pd
from dataCleanUp import removeNoReturn
import seaborn as sns

fontSize = 11
marker = ""
linewidth = 1

def getDataFrames(data, names):
    dates = []
    for d in data:
        dates.append(d['date'])
    dates = pd.to_datetime(dates)

    dataPoints = []
    for name in names:
        columnDataPoints = []
        for entry in data:
            if name == "posNeg":
                pos = entry["positiveSentiment"]
                if pos == 0:
                    pos = 0.0000000000000001
                columnDataPoints.append(entry["negativeSentiment"] / pos)
            else:
                columnDataPoints.append(entry[name])
        dataPoints.append(columnDataPoints)

    frames = []
    for i in range(len(names)):
        frames.append(pd.DataFrame(data=dataPoints[i], index=dates, columns=[names[i]]))

    return frames

def displayPriceVsSentiment(prices, sentiment, pricesColumns, sentimentColumns):
    prices = removeNoReturn(prices, pricesColumns)
    pricesFrames = getDataFrames(prices, pricesColumns)
    sentimentFrames = getDataFrames(sentiment, sentimentColumns)

    colourN = 0
    colours = sns.color_palette("muted", len(pricesColumns) + len(sentimentColumns))
    sns.set_style("white")

    fig, ax = plt.subplots()
    if len(pricesColumns) > 0:
        for f in pricesFrames:
            ax.plot(f, color=colours[colourN], marker=marker, linewidth=linewidth)
            colourN += 1
        ax.set_xlabel("date", fontsize=fontSize)
        ax.set_ylabel("price", fontsize=fontSize)
    elif len(sentimentColumns) > 0:
        for f in sentimentFrames:
            ax.plot(f, color=colours[colourN], marker=marker, linewidth=linewidth)
            colourN += 1
        ax.set_ylabel("sentiment", fontsize=fontSize)
    
    if len(sentimentColumns) > 0 and len(pricesColumns) > 0:
        ax2 = ax.twinx()
        for f in sentimentFrames:
            ax2.plot(f, color=colours[colourN], marker=marker, linewidth=linewidth)
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

def displayHist(x, bins, name):
    sns.set_style("white")
    sns.distplot(x, bins=bins)
    plt.xlabel(name)
    plt.ylabel("Frequency")
    plt.show()

def plot(x, y, legend):
    colours = sns.color_palette("muted", 2)
    sns.set_style("white")
    plt.plot(x, color=colours[0])
    plt.plot(y, color=colours[1])
    plt.legend(legend)
    plt.show()

def plotTimeAccuracy(data):
    colours = sns.color_palette("muted", 2)
    sns.set_style("white")
    fig, ax = plt.subplots()
    ax.bar([x[0] for x in data], [x[2] for x in data], color=colours[0])
    ax.set_xlabel("model")
    ax.set_ylabel("accuracy")
    ax2 = ax.twinx()
    ax2.plot([x[1] for x in data], color=colours[1])
    ax2.set_ylabel("time (ms)")
    fig.legend(["model", "time"])
    plt.show()