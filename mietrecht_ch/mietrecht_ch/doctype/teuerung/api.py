from calendar import month
from datetime import datetime, timedelta
import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.resultRow import ResultRow
from mietrecht_ch.models.resultTableDescription import ResultTableDescription
from mietrecht_ch.models.resultTable import ResultTable
from mietrecht_ch.models.teuerung import TeuerungInflationResult, TeuerungOldIndex, TeuerungNewIndex, FIELD_VALUE
from mietrecht_ch.utils.queryExecutor import execute_query
from mietrecht_ch.utils.dateUtils import buildFullDate, buildDatesInChronologicalOrder, swapDateIfNeeded


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
    converted_base_year_integer = __create_unique_basis_from_indexes__(
        indexes, base_year_integer)

    result = []
    for x in converted_base_year_integer:
        listTemp = []
        listTemp.append(x)
        listTemp.extend([y['value']
                        for y in indexes if y['base_year'] == str(x)])
        result.append(ResultRow(listTemp))

    result_table_description_iterated = [
        ResultTableDescription("auf der Basis", "number")]
    for x in last_five_months:
        result_table_description_iterated.append(
            ResultTableDescription(x, "number"))

    resultTable = ResultTable(result_table_description_iterated, result)

    calculatorResult = CalculatorResult(None, resultTable)

    return CalculatorMasterResult(
        None,
        [calculatorResult]
    )


@frappe.whitelist(allow_guest=True)
def get_inflation_for_period(basis: int, inflationRate: float, fromMonth: int, fromYear: int, toMonth: int, toYear: int):

    old_date_formatted = buildFullDate(fromYear, fromMonth)
    new_date_formatted = buildFullDate(toYear, toMonth)

    values_from_sql_query = __get_values_from_sql_query__(
        basis, old_date_formatted, new_date_formatted)

    results = __compute_result__(inflationRate, old_date_formatted, new_date_formatted, values_from_sql_query)

    calculatorResult = CalculatorResult(results, None)

    return CalculatorMasterResult(
        {'basis': basis, 'inflationRate': inflationRate, 'fromMonth': fromMonth,
            'fromYear': fromYear, 'toMonth': toMonth, 'toYear': toYear},
        [calculatorResult]
    )

def __compute_result__(inflationRate, old_date_formatted, new_date_formatted, values_from_sql_query):
    results = None
    if  values_from_sql_query and len(values_from_sql_query) == 2:
        old_index_value = values_from_sql_query[0][FIELD_VALUE]
        new_index_value = values_from_sql_query[1][FIELD_VALUE]

        rounded_inflation = __round_inflation_number__(
            old_index_value, new_index_value, inflationRate)

        results = __result_of_all_data__(
            old_date_formatted, old_index_value, new_date_formatted, new_index_value, rounded_inflation)
            
    return results


def __get_values_from_sql_query__(basis, old_date_formatted, new_date_formatted):
    order = 'asc' if old_date_formatted < new_date_formatted else 'desc'
    sql = execute_query(
        """select publish_date, base_year, value 
            from tabTeuerung 
            where base_year = '{basis}' and publish_date in ('{old_date_formatted}', '{new_date_formatted}') 
            order by publish_date {order}"""
        .format(basis=basis, old_date_formatted=old_date_formatted, new_date_formatted=new_date_formatted, order=order))
    return sql


def __result_of_all_data__(old_date_formatted, old_index_value, new_date_formatted, new_index_value, rounded_inflation):
    result = []
    result.append(TeuerungInflationResult(TeuerungOldIndex(old_date_formatted, old_index_value),
                  TeuerungNewIndex(new_date_formatted, new_index_value), rounded_inflation))
    return result


def __round_inflation_number__(old_index_value, new_index_value, inflation):
    number_not_rounded = (new_index_value - old_index_value) / \
        (old_index_value) * int(inflation)
    number_rounded = round(number_not_rounded, 2)
    return number_rounded


def __create_unique_basis_from_indexes__(indexes, baseYearIntegers):
    for i in indexes:
        baseYearIntegers.append(int(i.base_year))
    return sorted(set(baseYearIntegers), key=None, reverse=True)


def __get_last_five_months__():
    now = datetime.now()
    result = [now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)]
    for _ in range(0, 4):
        now = now.replace(day=1, hour=0, minute=0, second=0,
                          microsecond=0) - timedelta(days=1)
        result.append(now)
    return sorted(set(result))
