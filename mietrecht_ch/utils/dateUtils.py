from datetime import datetime
from dateutil.relativedelta import relativedelta

DATE_FORMAT = '%Y-%m-%d'


def buildFullDate(year, month, day="01"):
    return year + '-' + str.zfill(month, 2) + '-' + day


def swapDateIfNeeded(fromDate, toDate):
    if fromDate > toDate:
        return toDate, fromDate
    return fromDate, toDate


def buildDatesInChronologicalOrder(fromYear, fromMonth, toYear, toMonth, fromDay='01', toDay="01"):
    fromFull = buildFullDate(fromYear, fromMonth, fromDay)
    toFull = buildFullDate(toYear, toMonth, toDay)

    return swapDateIfNeeded(fromFull, toFull)


def date_with_month_ahead(date, number_of_months):
    date_format = '%Y-%m-%d'
    date_object = datetime.strptime(date, date_format)
    new_date = date_object + relativedelta(months=number_of_months)
    new_date_formatted = new_date.strftime(date_format)
    return new_date_formatted
