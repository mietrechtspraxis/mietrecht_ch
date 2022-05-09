DATE_FORMAT = '%Y-%m-%d'

def buildFullDate(year, month, day="01"):
    return year + '-' + str.zfill(month, 2) + '-' + day

def swapDateIfNeeded(fromDate, toDate):
    if fromDate > toDate :
        return toDate, fromDate
    return fromDate, toDate

def buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth, fromDay='01', toDay="01"):
    fromFull = buildFullDate(fromYear, fromMonth, fromDay)
    toFull = buildFullDate(toYear, toMonth, toDay)

    return swapDateIfNeeded(fromFull, toFull)