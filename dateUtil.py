import datetime

def getShortDateString(date):
    date = date.split()
    m = 0
    if date[0] == "Jan":
        m = 1
    elif date[0] == "Feb":
        m = 2
    elif date[0] == "Mar":
        m = 3
    elif date[0] == "Apr":
        m = 4
    elif date[0] == "May":
        m = 5
    elif date[0] == "Jun":
        m = 6
    elif date[0] == "Jul":
        m = 7
    elif date[0] == "Aug":
        m = 8
    elif date[0] == "Sep":
        m = 9
    elif date[0] == "Oct":
        m = 10
    elif date[0] == "Nov":
        m = 11
    elif date[0] == "Dec":
        m = 12
    if(len(date) == 2):
        y = int(date[1])
        d = 1
    else:
        y = int(date[2])
        d = int(date[1].split(",")[0])
    return datetime.datetime(y, m, d).strftime('%Y-%m-%d')

def getLongDateString(date):
    date = date.split()
    m = 0
    if date[0] == "January":
        m = 1
    elif date[0] == "February":
        m = 2
    elif date[0] == "March":
        m = 3
    elif date[0] == "April":
        m = 4
    elif date[0] == "May":
        m = 5
    elif date[0] == "June":
        m = 6
    elif date[0] == "July":
        m = 7
    elif date[0] == "August":
        m = 8
    elif date[0] == "September":
        m = 9
    elif date[0] == "October":
        m = 10
    elif date[0] == "November":
        m = 11
    elif date[0] == "December":
        m = 12
    if(len(date) == 2):
        y = int(date[1])
        d = 1
    else:
        y = int(date[2])
        d = int(date[1].split(",")[0])
    return datetime.datetime(y, m, d).strftime('%Y-%m-%d')

def getFullDashedDateString(date):
    y, m, d = [int("".join(x.split())) for x in date.split('-')]
    return datetime.datetime(y, m, d).strftime('%Y-%m-%d')

def getDashedDateTime(date):
    y, m, d = [int("".join(x.split())) for x in date.split('-')]
    return datetime.datetime(y, m, d)

def greaterThanDate(dateA, dateB):
    dtA = getDashedDateTime(dateA)
    dtB = getDashedDateTime(dateB)
    return dtA > dtB

def greaterThanOrEqualDate(dateA, dateB):
    dtA = getDashedDateTime(dateA)
    dtB = getDashedDateTime(dateB)
    return dtA >= dtB

def equalDate(dateA, dateB):
    dtA = getDashedDateTime(dateA)
    dtB = getDashedDateTime(dateB)
    return dtA == dtB