from calendar import month
from datetime import datetime, timedelta
from datetime import date
from typing import List
from webbrowser import get
import frappe
# from mietrecht_ch.models.teuerung import TeuerungEntry
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultTable import ResultTable
from dateutil.relativedelta import relativedelta
from mietrecht_ch.utils.queryExecutor import execute_query
import itertools


@frappe.whitelist(allow_guest=True)
def get_last_five_indexes():

    lastFivePublishDates = execute_query(
        """select distinct(publish_date) from tabTeuerung where DAY(publish_date) = 1 order by publish_date desc LIMIT 5;""")

    inClause = ','.join(map(lambda x: "'{}'".format(
        x['publish_date'].strftime('%Y-%m-%d')), lastFivePublishDates))

    indexes = execute_query(
        """select base_year, publish_date, value from tabTeuerung where publish_date IN ({inClause}) order by base_year DESC, publish_date""".format(inClause=inClause))

    last_five_months = __get_last_five_months__()


    base_year_integer = []
    converted_base_year_integer = __create_integer__(indexes, base_year_integer)

    result = dict()
    for x in converted_base_year_integer:
        dictTemp = dict()
        dictTemp['base_year'] = x
        dictTemp['value'] = [y['value'] for y in indexes if y['base_year'] == str(x)]
        result[str(x)] = dictTemp

    resultTableDescriptions = [
        ResultTableDescription([last_five_months], "number")
    ]

    resultTable = ResultTable(resultTableDescriptions, result)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {'teueroung': '1914'},
        [calculatorResult]
    )


def __create_integer__(indexes, baseYearIntegers):
    for i in indexes:
        baseYearIntegers.append(int(i.base_year))
    return sorted(set(baseYearIntegers), key=None, reverse=True)

def __get_last_five_months__():
    now = datetime.now()
    result = [now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)]
    for _ in range(0, 4):
        now = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        result.append(now)
    return result

# def __structured_last_five_months__(convertedBaseYearInteger, last_five_months):
#     result_description = dict()
#     for y in itertools.islice(convertedBaseYearInteger, 5):
#         dict_description = dict()
#         dict_description['base_year'] = [x for x in last_five_months]
#         result_description[str(y)] = dict_description

#     return result_description