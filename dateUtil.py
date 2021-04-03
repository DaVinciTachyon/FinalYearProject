import datetime

def getDateTime(date):
    y, m, d = [int(x) for x in date.split('-')]
    return datetime.datetime(y, m, d)

def greaterThanDate(dateA, dateB):
    dtA = getDateTime(dateA)
    dtB = getDateTime(dateB)
    return dtA > dtB

def greaterThanOrEqualDate(dateA, dateB):
    dtA = getDateTime(dateA)
    dtB = getDateTime(dateB)
    return dtA >= dtB

def equalDate(dateA, dateB):
    dtA = getDateTime(dateA)
    dtB = getDateTime(dateB)
    return dtA == dtB