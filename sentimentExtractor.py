# TODO uses proquest. should use lexis nexis?
# TODO currently grabs entire article...differentiation between texts?

# source = 'proquest'
source = 'lexisnexis'

def getDictionary():
    import pandas as pd

    data = pd.read_excel (r"./dictionaries/inquirerbasic.xls") 
    df = pd.DataFrame(data, columns= ['Entry', 'Positiv', 'Negativ']).to_numpy()
    dictionary = {}
    for index, item in enumerate(df):
        dictionary[item[0]] = item[1:]
    return dictionary

def getArticles():
    if(source == 'proquest'):
        from os import walk

        path = './proquest/'
        _, _, filenames = next(walk(path))

        articles = []

        for f in filenames:
            files = open(path + f, 'r')
            content = files.read()
            a = content.split('____________________________________________________________')
            a = list(map(str.strip, a))
            articles.extend(a[1:-1])
            files.close()
    elif(source == 'lexisnexis'):
        files = open('./lexisnexis_out.txt', 'r')
        content = files.read()
        a = content.split('____________________________________________________________')
        a = list(map(str.strip, a))
        articles = a[:-1]
        files.close()
    return articles

def getArticleDate(article):
    if(source == 'proquest'):
        line = [s for s in article.splitlines() if 'Last updated' in s]
        return "".join(line[0].split(':')[1].strip().split())
    elif(source == 'lexisnexis'):
        line = [s for s in article.splitlines() if 'LOAD-DATE' in s]
        textDate = line[0].split(':')[1].strip().split()
        textDate[1] = textDate[1].split(",")[0]
        if(textDate[0] == "January"):
            month = 1
        elif(textDate[0] == "February"):
            month = 2
        elif(textDate[0] == "March"):
            month = 3
        elif(textDate[0] == "April"):
            month = 4
        elif(textDate[0] == "May"):
            month = 5
        elif(textDate[0] == "June"):
            month = 6
        elif(textDate[0] == "July"):
            month = 7
        elif(textDate[0] == "August"):
            month = 8
        elif(textDate[0] == "September"):
            month = 9
        elif(textDate[0] == "October"):
            month = 10
        elif(textDate[0] == "November"):
            month = 11
        elif(textDate[0] == "December"):
            month = 12
        return textDate[2] + "-" + f"{month:0>2}" + "-" + f"{textDate[1]:0>2}"

def getArticleAnalysis(articles, dictionary):
    import numpy as np

    breakdowns = []

    for a in articles:
        date = getArticleDate(a)
        words = a.split()
        total = len(words)
        positive = 0
        negative = 0
        for word in words:
            upperWord = word.upper()
            if upperWord in dictionary:
                attributes = dictionary[upperWord]
                if 'Positiv' in attributes:
                    positive += 1
                if 'Negativ' in attributes:
                    negative += 1
        breakdowns.append({ 'date': date, 'totalWords': total, 'positiveSentiment': positive, 'negativeSentiment': negative })
    
    return breakdowns

def getZScores(sentiment):
    dates = []
    articles = []
    totalWords = []
    positiveSentiment = []
    negativeSentiment = []
    for s in sentiment:
        dates.append(s['date'])
        articles.append(s['articles'])
        totalWords.append(s['totalWords'])
        positiveSentiment.append(s['positiveSentiment'])
        negativeSentiment.append(s['negativeSentiment'])

    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    for i in range(len(negativeSentiment)):
        negativeSentiment[i] = np.round((negativeSentiment[i] * 100.0) / totalWords[i], decimals=2)
    for i in range(len(positiveSentiment)):
        positiveSentiment[i] = np.round((positiveSentiment[i] * 100.0) / totalWords[i], decimals=2)
    for i in range(len(totalWords)):
        totalWords[i] = np.round((totalWords[i] * 100.0) / articles[i], decimals=2)
    totalWords = stats.zscore(totalWords)
    negativeSentiment = stats.zscore(negativeSentiment)
    positiveSentiment = stats.zscore(positiveSentiment)

    zScoreSentiment = []
    for i in range(len(sentiment)):
        zScoreSentiment.append({ 'date': dates[i], 'articles': articles[i], 'totalWords': np.round(totalWords[i], decimals=2), 'positiveSentiment': np.round(positiveSentiment[i], decimals=2), 'negativeSentiment': np.round(negativeSentiment[i], decimals=2) })
    return zScoreSentiment

def getArticleSentiment():
    dictionary = getDictionary()
    articles = getArticles()
    return getArticleAnalysis(articles, dictionary)

def getArticleSentimentByDate():
    sentiment = getArticleSentiment()
    sentimentByDate = []
    for i in range(len(sentiment)):
        included = False
        entry = sentiment[i]
        date = entry['date']
        for secondaryEntry in sentimentByDate:
            if date == secondaryEntry['date']:
                included = True
                break
        if not included:
            articles = 1
            total = entry['totalWords']
            positive = entry['positiveSentiment']
            negative = entry['negativeSentiment']
            for j in range(i + 1, len(sentiment)):
                secondaryEntry = sentiment[j]
                if date == secondaryEntry['date']:
                    articles += 1
                    total += secondaryEntry['totalWords']
                    positive += secondaryEntry['positiveSentiment']
                    negative += secondaryEntry['negativeSentiment']
            sentimentByDate.append({ 'date': date, 'articles': articles, 'totalWords': total, 'positiveSentiment': positive, 'negativeSentiment': negative })
    import operator
    sentimentByDate = sorted(sentimentByDate, key = operator.itemgetter('date'))
    return getZScores(sentimentByDate)
