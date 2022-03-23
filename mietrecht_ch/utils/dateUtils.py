def buildFullDate(year, month):
    return year + '-' + str.zfill(month, 2) + '-01'

def build_day_month_year_date(year, month):
    return '01' + '-' + month + '-' + year

def swapDateIfNeeded(fromDate, toDate):
    if fromDate > toDate :
        return toDate, fromDate
    return fromDate, toDate

def buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth):
    fromFull = buildFullDate(fromYear, fromMonth)
    toFull = buildFullDate(toYear, toMonth)

    return swapDateIfNeeded(fromFull, toFull)