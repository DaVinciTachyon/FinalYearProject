# The sentiment extractor gathers articles and extracts sentiment from them,
# this is done by analysing word choices.
# This may extract different features as well,
# such as negative vs positive sentiment, as required later on.
# It is currently going to be inspired by rocksteady.
# In theory rocksteady may be used, however, it may be more beneficial to create a version myself.
# This is yet to be fully decided. This will allow the process to be streamlined.
# However, I will look into seeing which one will be the right choice. The articles will be sources from proquest.

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
    line = [s for s in articles[0].splitlines() if 'Last updated' in s]
    date = line[0].split(':')[1].strip().split('-')
    date = [int(s) for s in date]
    return [date[2], date[1], date[0]]

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
        breakdowns.append([date, total, positive, negative])
    
    return breakdowns

dictionary = getDictionary()
articles = getArticles()
print(getArticleAnalysis(articles, dictionary))