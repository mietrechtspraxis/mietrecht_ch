from calendar import month
from datetime import datetime, timedelta
from datetime import date
from typing import List
from webbrowser import get
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultTable import ResultTable
from dateutil.relativedelta import relativedelta
from mietrecht_ch.utils.queryExecutor import execute_query
import itertools


@frappe.whitelist(allow_guest=True)
def get_last_five_indexes():

    last_five_publish_dates = execute_query(
        """select distinct(publish_date) from tabTeuerung where DAY(publish_date) = 1 order by publish_date desc LIMIT 5;""")

    inClause = ','.join(map(lambda x: "'{}'".format(
        x['publish_date'].strftime('%Y-%m-%d')), last_five_publish_dates))

    indexes = execute_query(
        """select base_year, publish_date, value from tabTeuerung where publish_date IN ({inClause}) order by base_year DESC, publish_date""".format(inClause=inClause))

    last_five_months = __get_last_five_months__()


    base_year_integer = []
    converted_base_year_integer = __create_unique_basis_from_indexes__(indexes, base_year_integer)

    result = []
    for x in converted_base_year_integer:
        listTemp = []
        listTemp.append(x)
        listTemp.extend([y['value'] for y in indexes if y['base_year'] == str(x)])
        result.append(listTemp)

    result_table_description_iterated = []
    for x in last_five_months:
        result_table_description_iterated.append(ResultTableDescription([x], "number"))
       

    resultTable = ResultTable(result_table_description_iterated, result)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        {None},
        [calculatorResult]
    )


def __create_unique_basis_from_indexes__(indexes, baseYearIntegers):
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