# TODO uses proquest. should use lexis nexis?
# TODO currently grabs entire article...differentiation between texts?

def getDictionary():
    import pandas as pd

    data = pd.read_excel (r"./dictionaries/inquirerbasic.xls") 
    df = pd.DataFrame(data, columns= ['Entry', 'Positiv', 'Negativ']).to_numpy()
    dictionary = {}
    for index, item in enumerate(df):
        dictionary[item[0]] = item[1:]
    return dictionary

def getArticles():
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
    return articles

def getArticleDate(article):
    line = [s for s in article.splitlines() if 'Last updated' in s]
    return "".join(line[0].split(':')[1].strip().split())

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
    return sorted(sentimentByDate, key = operator.itemgetter('date'))
