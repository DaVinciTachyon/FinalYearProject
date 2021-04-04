from os import listdir, walk
from os.path import isfile, join
from striprtf.striprtf import rtf_to_text
from datetime import datetime
import copy
import json
import sys
from dateUtil import getShortDateString, getFullDashedDateString, getLongDateString
import pandas as pd
import numpy as np
import scipy.stats as stats

this = sys.modules[__name__]
this.source = "lexisnexis"

def setSource(s):
    this.source = s

documentTemplate = {
    'title': '',
    'source': 'Unknown Newspaper',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'copyright': 'Copyright None Found',
    'length': 0,
    'section': 'A,A; Pg 1',
    'language': 'ENGLISH',
    'pubtype': 'Newspaper',
    'subject': '',
    'geographic': '',
    'loaddate': datetime.now().strftime('%Y-%m-%d'),
    'byline': 'No Author',
    'body': ''
}

def getDictionary():
    import pandas as pd

    data = pd.read_excel(r"./dictionaries/inquirerbasic.xls") 
    df = pd.DataFrame(data, columns= ['Entry', 'Positiv', 'Negativ']).to_numpy()
    dictionary = {}
    for index, item in enumerate(df):
        dictionary[item[0]] = item[1:]
    return dictionary

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
        positive = 0
        negative = 0
        for word in a['body'].split():
            upperWord = word.upper()
            if upperWord in dictionary:
                attributes = dictionary[upperWord]
                if 'Positiv' in attributes:
                    positive += 1
                if 'Negativ' in attributes:
                    negative += 1
        breakdowns.append({ 'date': a['date'], 'totalWords': a['length'], 'positiveSentiment': positive, 'negativeSentiment': negative })
    
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

    for i in range(len(negativeSentiment)):
        if totalWords[i] > 0:
            negativeSentiment[i] = np.round((negativeSentiment[i] * 100.0) / totalWords[i], decimals=2)
        else:
            negativeSentiment[i] = 0
    for i in range(len(positiveSentiment)):
        if totalWords[i] > 0:
            positiveSentiment[i] = np.round((positiveSentiment[i] * 100.0) / totalWords[i], decimals=2)
        else:
            positiveSentiment[i] = 0
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
    articles = extractArticles()
    return getArticleAnalysis(articles, dictionary)

def getArticleSentimentByDate():
    if isfile(f"./articles/{source}/output/sentiment.json"):
        with open(f"./articles/{source}/output/sentiment.json") as json_file:
            zscores = json.load(json_file)
    else:
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
        zscores = getZScores(sentimentByDate)
        with open(f"./articles/{source}/output/sentiment.json", 'w') as json_file:
            json.dump(zscores, json_file)
    return zscores

def extractArticles():
    if isfile(f"./articles/{source}/output/articles.json"):
        with open(f"./articles/{source}/output/articles.json") as json_file:
            documents = json.load(json_file)
    else:
        path = f"./articles/{source}/input/"
        files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        if len(files) == 0:
            print(f"No files in the directory {path}")
            os.exit(1)

        documents = []
        if source == 'lexisnexis':
            i = 0
            for f in files:
                reader = ReadInputFile(f)
                text = reader.readFileContents()
                parsedText = rtf_to_text(text)
                documents.extend(parseDocumentsFromRTF(parsedText))
                i += 500
                print(i)
        elif source == 'proquest':
            i = 0
            for f in files:
                file = open(f, 'r')
                text = file.read()
                documents.extend(parsedDocumentsFromTXT(text))
                file.close()
                i += 50
                print(i)
        with open(f"./articles/{source}/output/articles.json", 'w') as json_file:
            json.dump(documents, json_file)

    return documents

def parsedDocumentsFromTXT(text):
    articles = text.split('____________________________________________________________')
    articles = list(map(str.strip, articles))[1:-1]
    parsedArticles = []
    for article in articles:
        isBody = False
        document = copy.deepcopy(documentTemplate)
        body = ""
        for line in article.splitlines():
            tempLine = line.strip()
            if tempLine == '':
                continue
            if tempLine.startswith('Full text: ') :
                isBody = True
                continue
            if isBody and tempLine.startswith('Subject: '):
                document['body'] = body
                document['length'] = len(body.split())
                isBody = False
            if isBody:
                body += line + '\n'
                continue
            if tempLine.startswith('Title: ') and extractValue(line) != '':
                document['title'] = extractValue(line)
                continue
            if tempLine.startswith('Source type: ') and extractValue(line) != '':
                document['source'] = extractValue(line)
                continue
            if tempLine.startswith('Publication date: ') and extractValue(line) != '':
                document['date'] = getShortDateString(extractValue(line))
                continue
            if tempLine.startswith('Copyright: ') and extractValue(line) != '':
                document['copyright'] = extractValue(line)
                continue
            if tempLine.startswith('Language of publication: ') and extractValue(line) != '':
                document['language'] = extractValue(line).upper()
                continue
            if tempLine.startswith('Document type: ') and extractValue(line) != '':
                document['pubtype'] = extractValue(line)
                continue
            if tempLine.startswith('Subject: ') and extractValue(line) != '':
                document['subject'] = extractValue(line)
                continue
            if tempLine.startswith('Country of publication: ') and extractValue(line) != '':
                document['geographic'] = extractValue(line)
                continue
            if tempLine.startswith('Last updated: ') and extractValue(line) != '':
                document['loaddate'] = getFullDashedDateString(extractValue(line))
                continue 
            if tempLine.startswith('Publisher: ') and extractValue(line) != '':
                document['byline'] = extractValue(line)
                continue
        parsedArticles.append(document)
    return parsedArticles

class ReadInputFile:
    def __init__(self, filename):
        self.filename = filename

    def readFileContents(self):
        fileContent = ''
        try:
            with open(self.filename, 'r', encoding='utf8') as file:
                fileContent = "".join([f"{line}\n" if line.strip() != '' else f"{line}" for line in file])
            return fileContent
        except Exception as e:
            print(f'Error in reading the file {self.filename}. Error = {e}')
            return None

def parseDocumentsFromRTF(parsedText):
    documents = []
    docBody = False
    firstLineOfBody = False
    body = ''
    document = copy.deepcopy(documentTemplate)
    for line in parsedText.splitlines():
        tempLine = line.strip()
        if tempLine == '':
            continue
        if firstLineOfBody:
            document['title'] = line
            firstLineOfBody = False
            continue
        if tempLine.startswith('Source:') and extractValue(line) != '':
            document['source'] = extractValue(line)
            continue
        if tempLine.startswith('Copyright '):
            document['copyright'] = line
            continue
        if tempLine.startswith('Section:') and extractValue(line) != '':
            document['section'] = extractValue(line)
            continue
        if tempLine.startswith('Language:') and extractValue(line) != '':
            document['language'] = extractValue(line)
            continue
        if tempLine.startswith('Publication-Type:') and extractValue(line) != '':
            document['pubtype'] = extractValue(line)
            continue
        if tempLine.startswith('Subject:') and extractValue(line) != '':
            document['subject'] = extractValue(line)
            continue
        if tempLine.startswith('Geographic:') and extractValue(line) != '':
            document['geographic'] = extractValue(line)
            continue
        if tempLine.startswith('Load-Date:') and extractValue(line) != '':
            date = getLongDateString(extractValue(line))
            document['loaddate'] = date
            document['date'] = date
            document['body'] = body
            document['length'] = len(body.split())
            body = ''
            docBody = False
            continue
        if tempLine.startswith('Byline:') and extractValue(line) != '':
            document['byline'] = extractValue(line)
            continue
        if tempLine == 'Body':
            body = ''
            docBody = True
            firstLineOfBody = True
            continue
        if tempLine.startswith('[readmore]'):
            continue
        if tempLine == 'End of Document':
            documents.append(document)
            document = copy.deepcopy(documentTemplate)
            continue
        if docBody:
            body += line + '\n'
            continue
    return documents

def extractValue(data):
    if ':' in data:
        return data.split(':')[1].strip()
    else:
        return data.strip()