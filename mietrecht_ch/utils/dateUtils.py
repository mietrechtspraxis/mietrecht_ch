def buildFullDate(year, month):
    return year + '-' + str.zfill(month, 2) + '-01'

def swapDateIfNeeded(fromDate, toDate):
    if fromDate > toDate :
        return toDate, fromDate
    return fromDate, toDate